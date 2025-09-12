from bs4 import BeautifulSoup
import glob

# Path to your HTML files (adjust the pattern as needed)
html_files = glob.glob("1/OEBPS/*.html")
html_files.sort()
# Create an empty BeautifulSoup object for the final merged document
merged_soup = None

for i, file in enumerate(html_files):
    with open(file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        if i % 200 == 0:
            if i != 0:
                with open(f"merged{i}.html", "w", encoding="utf-8") as f_out:
                    f_out.write(str(merged_soup))
            # Use the first file as the base
            merged_soup = BeautifulSoup(str(soup), "html.parser")
            merged_body = merged_soup.body
        else:
            # Append the body content of subsequent files
            body_content = soup.body.contents if soup.body else []
            #assert len(body_content) == 1, len(body_content)
            for element in body_content:
                if str(element) == '\n':
                  continue
                merged_body = merged_body.append(element)

