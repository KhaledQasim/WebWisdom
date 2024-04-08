import subprocess




def get_vulnerability_report(url):
    
    # Simulating a function that returns the report as a string.
    # Replace this with your actual function that retrieves the report.
    # Command to be executed, as a single string
    command = f'ptt -q run website_scanner {url}'

    # Running the command
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    print(result.stdout)
    return result.stdout




def parse_vulnerability_report_for_technologies(report_text:str):
    lines = report_text.split('\n')
    in_technology_section = False
    technologies = []
    i = 0  # Line index

    while i < len(lines):
        line = lines[i].strip()
        
        if 'Server software and technology found' in line:
            in_technology_section = True
            i += 1
            continue
        
        # if in_technology_section and line.startswith('[') and not line.startswith('[2]'):
        if in_technology_section and line.startswith('['):

            # Exit the loop if the next section is reached
            break
        
        if in_technology_section and '- Evidence' in line:
            technology = {}
            while True:
                i += 1
                if i >= len(lines):
                    break
                line = lines[i].strip()

                if line.startswith('- Software / Version:'):
                    software_version_full = line.split(':', 1)[1].strip()
                    # Attempt to split software name and version. Assumes version is last and separated by space.
                    parts = software_version_full.rsplit(' ', 1)
                    if len(parts) == 2 and any(char.isdigit() for char in parts[1]):
                        # Checks if the last part has any digit, assuming it's a version number.
                        technology['software_name'], technology['software_version'] = parts
                    else:
                        # If there's no discernible version (no space-separated part with a digit),
                        # treat the whole string as the name and mark version as "Unknown".
                        technology['software_name'] = software_version_full
                        technology['software_version'] = "Unknown"
                elif line.startswith('- Category:'):
                    technology['category'] = line.split(':', 1)[1].strip()
                elif line.startswith('[') or line.startswith('- Evidence') or line.strip() == '':
                    # Break if another evidence starts or if an unrelated line is reached
                    break

            technologies.append(technology)
            
            continue  # Skip the increment at the end of the loop since we've already moved to the next line
        
        i += 1  # Move to the next line
        
    # removing any empty dictionaries at the end of the list
    technologies = [technology for technology in technologies if technology]
    return technologies



def formate_report(url):
    print("urlhere",url)
    report_text = get_vulnerability_report(url)
    technologies = parse_vulnerability_report_for_technologies(report_text)
    return {"technologies":technologies}