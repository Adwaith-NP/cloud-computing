import docker

def create_and_interact_with_ubuntu(size=1):
    try:
        # Initialize Docker client
        client = docker.from_env()

        # Pull the Ubuntu image
        print("Pulling Ubuntu image...")
        client.images.pull("ubuntu")
        # Convert size from "10G" to bytes for Docker tmpfs option
        size_in_mb = size * 1024

        # Create and start an Ubuntu container with resource limits
        print("Creating Ubuntu container with CPU, memory, and storage limits...")
        container = client.containers.run(
            "ubuntu",
            name="demo_ubuntu",
            stdin_open=True,  # Keep STDIN open for input
            tty=True,         # Allocate a pseudo-TTY
            detach=True,      # Run container in detached mode
            cpu_period=100000,  # Define base CPU period
            cpu_quota=200000,   # Allocate 2 CPU threads (200%)
            mem_limit="512m",    # Set memory limit to 512MB
            tmpfs={"/mnt/data": f"size={size_in_mb}m"}  
        )

        print("Ubuntu container started!")
        print("You can interact with the Ubuntu CLI below (type 'exit' to quit).")
        print(f"The {size} storage volume is mounted at /mnt/data.")

        # Attach to the container for interactive I/O
        while True:
            user_command = input("ubuntu> ")

            if user_command.lower() in ["exit", "quit"]:
                print("Exiting Ubuntu CLI...")
                break

            exec_result = container.exec_run(user_command, tty=True)
            output = exec_result.output.decode("utf-8")
            print(output)

        # Stop and remove the container after exiting
        container.stop()
        container.remove()
        print("Container stopped and removed.")

    except Exception as e:
        print(f"Unexpected error: {e}")
        

def interactive_shell(container_name):
    client = docker.from_env()

    try:
        # Get the container
        container = client.containers.get(container_name)
        print(f"Connected to container: {container_name}")

        # Start interactive command loop
        while True:
            user_command = input("ubuntu> ")

            if user_command.lower() in ["exit", "quit"]:
                print("Exiting Ubuntu CLI...")
                break

            # Execute the command inside the container
            exec_id = client.api.exec_create(
                container.id, 
                cmd=user_command, 
                stdin=True, 
                tty=True
            )
            exec_result = client.api.exec_start(exec_id, tty=True)

            # Display the output
            print(exec_result.decode("utf-8"))

    except docker.errors.NotFound:
        print(f"Error: Container '{container_name}' not found.")
    except Exception as e:
        print(f"Unexpected error: {e}")


# Usage Example



if __name__ == "__main__":
    # size = input("Enter the size for the Ubuntu storage volume : ")
    interactive_shell("demo_ubuntu")
    # create_and_interact_with_ubuntu(size=size)

