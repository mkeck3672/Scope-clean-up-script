import subprocess
import os


def process_json(json_file, output_folder, output_file, num_lines):
    try:
        # Execute the command using subprocess
        command = f'grep -o \'"host": "[^"]*"\' {json_file} | awk -F\'"\' \'{{print $4}}\' | awk \'{{gsub(/[\^\\\\$]/,"")}}1\' | sort -u'
        output = subprocess.check_output(command, shell=True, text=True)

        # Split the output into lines
        lines = output.splitlines()

        # Limit the lines based on user input
        lines = lines[:num_lines]

        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Save the results to a text file in the specified folder
        output_file_path = os.path.join(output_folder, output_file)
        with open(output_file_path, 'w') as f:
            f.write('\n'.join(lines))

        print(
            f"Processed {json_file} and saved the first {num_lines} lines to {output_file_path}")

        # If there are more lines, create additional files
        if len(lines) < len(output.splitlines()):
            file_count = 1
            while lines:
                lines = output.splitlines(
                )[file_count * num_lines: (file_count + 1) * num_lines]
                if lines:
                    output_file = f"{json_file.replace('.json', '')}_{file_count}.txt"
                    output_file_path = os.path.join(output_folder, output_file)
                    with open(output_file_path, 'w') as f:
                        f.write('\n'.join(lines))
                    print(
                        f"Saved the next {num_lines} lines to {output_file_path}")
                file_count += 1
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Get user input for the JSON file name
    json_file = input("Enter the name of the JSON file (e.g., test.json): ")

    # Get user input for the output folder name
    output_folder = input("Enter the name of the output folder: ")

    # Get user input for the output file name
    output_file = input("Enter the name of the output file (e.g., moretest): ")

    # Get user input for the number of lines
    num_lines = int(input("Enter the number of lines to limit the output: "))

    # Call the function to process the JSON file
    process_json(json_file, output_folder, output_file, num_lines)
