import docker
import subprocess
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
        try:
            # Get the container
            subprocess.run(["docker", "exec", "-it", container.id, "bash"])
        except KeyError as e:
            print("Error : ",e)

        # Stop and remove the container after exiting
        # container.stop()
        # container.remove()
        # print("Container stopped and removed.")

    except Exception as e:
        print(f"Unexpected error: {e}")
        

def interactive_shell(container_name):
    client = docker.from_env()

    try:
        # Get the container
        container = client.containers.get(container_name)
        container.start()
        print(f"Connected to container: {container_name}")
        subprocess.run(["docker", "exec", "-it", container.id, "bash"])
        choice  = input("To delete type(del)/to stop type(stp)/else(just enter)")
        if choice == "del":
            container.stop()
            container.remove()
        elif choice == "stp":
            container.stop()
        
    except KeyError as e:
        print("Error : ",e)


# Usage Example

def container_update(container_name,):
    client = docker.from_env()
    container = client.containers.get(container_name)
    
    image = container.image.tags[0]  # Get the image tag
    name = container.name
    
    # Stop and remove the existing container
    container.stop()
    container.remove()
    
    # Create a new container with updated tmpfs
    tmpfs_size = 50000
    new_container = client.containers.run(
        image,
        name=name,
        stdin_open=True,
        tty=True,
        detach=True,
        cpu_quota=100000,  # 1 CPU
        cpu_period=100000, # Keep period unchanged
        mem_limit="512m",  # Reduce memory to 512MB
        tmpfs={"/mnt/data": f"size={tmpfs_size}m"}  # Updated tmpfs size
    )
    
    print(f"Recreated container '{new_container.name}' with updated tmpfs.")

if __name__ == "__main__":
    choice = input()
    if choice == "1":
        size = input("Enter the size for the Ubuntu storage volume : ")
        create_and_interact_with_ubuntu(size=size)
    elif choice == "2":
        interactive_shell("demo_ubuntu")
    elif choice == "3":
        container_update("demo_ubuntu")
    # 

