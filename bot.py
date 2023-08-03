import requests
import os
import json

repo = os.getenv("REPO")
owner = os.getenv("OWNER")
function_url = os.getenv("FUNCTION_URL")


def invoke_vuln_function():
    """this function invokes the vuln function"""

    vuln_data = json.load(open("sbom-report"))
    data = {
        "repo": repo,
        "owner": owner,
        "vulnerabilities": vuln_data["vulnerabilities"]
    }

    url = f"{function_url}"
    response = requests.post(url, json=data)

    return response


if __name__ == "__main__":
    print(invoke_vuln_function())
