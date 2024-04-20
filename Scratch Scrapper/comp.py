import os
import zipfile

def compress_parent_to_zip():
    # Get the path of the parent directory
    parent_dir = os.path.dirname(__file__)
    
    # Define the name of the zip file
    zip_filename = os.path.join(parent_dir, 'parent_file.zip')
    
    # Initialize a ZipFile object to write to
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        # Walk through all the files and directories in the parent directory
        for root, dirs, files in os.walk(parent_dir):
            # Exclude the zip file itself from being included in the archive
            if root != os.path.dirname(zip_filename):
                # Add each file to the zip archive
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, parent_dir))

    print(f"Compression complete. Zip file saved as: {zip_filename}")

# Call the function to compress the parent directory
compress_parent_to_zip()
