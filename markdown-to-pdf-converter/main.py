import os
import markdown
import pdfkit
import re

# directory_path = "../files/examples"
directory_path = "../files/official-website"
output_name = "docs"
# content_title = "ReScript Code Examples"
content_title = "ReScript Documentation"
# content_intro = "This document contains a collection of code examples in ReScript."
content_intro = "This document contains the complete official documentation of ReScript version 11 as of December 2023."

def decrease_header_level(md_text):
    """
    Decreases each Markdown header level by two.
    """
    def replace_header(match):
        header, title = match.groups()
        if 'section' in title.lower():
            return f"{header} {title}"
        new_header = "#" * (len(header) + 2)
        return f"{new_header} {title}"

    return re.sub(r"(#{1,6})\s+(.*)", replace_header, md_text)
       

def convert_markdown_to_pdf(input_directory, output_pdf):
    # Title and Description of the output content file.
    title = "<h1>" + content_title + "</h1>"
    intro = "<p>" + content_intro + "</p>"

    combined_html = title + intro
    options = {"no-images": "", "quiet": ""}

    # CSS to wrap lines
    css = "<style>body {word-wrap: break-word;}</style>"

    # Iterate over each directory and file using os.walk
    for root, dirs, files in os.walk(input_directory):
        directory_name = os.path.basename(root)
        # Skip if directory_name is empty
        if directory_name:
            combined_html += f"<h1>SECTION {directory_name.upper()}</h1>"

        # Loop through all Markdown files
        for filename in files:
            if filename.endswith(".md") or filename.endswith(".mdx"):
                file_path = os.path.join(root, filename)

                # Use filename as the section title (excluding the .md extension)
                section_title = os.path.splitext(filename)[0]
                header = f"<h2>SECTION {section_title}</h2>"

                # Read and convert each Markdown file to HTML
                with open(file_path, "r") as file:
                    md_text = file.read()
                    updated_md_text = decrease_header_level(md_text)
                    html = markdown.markdown(
                        updated_md_text, extensions=["extra", "codehilite"]
                    )
                    combined_html += header + html

    # Combine CSS with HTML content
    final_html = css + combined_html

    # After converting Markdown to HTML
    with open(output_name + ".html", "w") as html_output_file:
        html_output_file.write(final_html)

    # Convert the combined HTML content to a single PDF
    pdfkit.from_string(final_html, output_pdf, options=options)


if __name__ == "__main__":
    input_directory = directory_path
    output_pdf = output_name + ".pdf"
    convert_markdown_to_pdf(input_directory, output_pdf)
