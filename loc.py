import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def count_loc_in_file(file_path):
    loc_count = 0
    is_in_block_comment = False
    
    # Define comment delimiters for different file types
    single_line_comment_start = {
        ".py": "#",
        ".c": "//",
        ".h": "//"
    }
    block_comment_start = {
        ".c": "/*",
        ".h": "/*"
    }
    block_comment_end = {
        ".c": "*/",
        ".h": "*/"
    }
    
    # Determine file extension to handle comments properly
    _, ext = os.path.splitext(file_path)
    
    # Open the file and count lines of code
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            stripped_line = line.strip()
            
            # Check for block comments
            if is_in_block_comment:
                # Check if we end the block comment
                if block_comment_end.get(ext, '') and block_comment_end[ext] in stripped_line:
                    is_in_block_comment = False
                continue
            
            # Check for starting a block comment
            if block_comment_start.get(ext, '') and block_comment_start[ext] in stripped_line:
                is_in_block_comment = True
                continue
            
            # Check if line is a comment or empty line
            if (single_line_comment_start.get(ext, '') and stripped_line.startswith(single_line_comment_start[ext])) or not stripped_line:
                continue
            
            # Line is counted as a line of code
            loc_count += 1
    
    return loc_count

def count_lines_of_code(directory):
    total_loc = 0
    c_and_python_files = ('.c', '.h', '.py')
    
    # Iterate through all files in the specified directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(c_and_python_files):
                file_path = os.path.join(root, file)
                # Count lines of code in the file
                total_loc += count_loc_in_file(file_path)
    
    return total_loc

def log_loc_to_file(loc, log_file_path):
    # Generate the timestamp and LOC information
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp}: Total lines of code: {loc}\n"
    
    # Write or append to the log file
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write(log_entry)
    
    print(f"Logged LOC to {log_file_path}")

def send_email(subject, body, to_email):
    # Your email configuration
    from_email = "example@example.com"
    password = ""

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    # Add the body text
    msg.attach(MIMEText(body, 'plain'))

    # Set up the server
    server = smtplib.SMTP('smtp.example.com', 587)  # Change smtp.example.com and port if needed
    server.starttls()
    
    try:
        # Login to the email server
        server.login(from_email, password)
        
        # Send the email
        server.sendmail(from_email, to_email, msg.as_string())
        
        print(f"Email sent to {to_email} successfully.")
    
    except Exception as e:
        print(f"Failed to send email: {e}")
    
    finally:
        # Close the server connection
        server.quit()

def main():
    # Specify the directory containing the C and Python files
    directory = 'path/to/directory'
    # Specify the log file path
    log_file_path = 'path/to/logfile'
    
    # Count lines of code excluding comments and empty lines
    total_loc = count_lines_of_code(directory)
    
    # Create the email body
    email_body = f'Total lines of code in {directory}: {total_loc}'
    
    # Send the email
    send_email('LOC Report', email_body, 'example@example.com')
    
    # Log the LOC to a text file
    log_loc_to_file(total_loc, log_file_path)

if __name__ == "__main__":
    main()
