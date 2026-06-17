import requests

def get_rxcui(medicine_name):
    """
    Convert medicine name to RxCUI code using RxNorm API.
    This API still works fine.
    """
    url = "https://rxnav.nlm.nih.gov/REST/rxcui.json"
    params = {"name": medicine_name}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        rxcui = data["idGroup"].get("rxnormId")
        if rxcui:
            return rxcui[0]
        else:
            return None
    except Exception as e:
        print(f"Error getting RxCUI for {medicine_name}: {e}")
        return None


def check_interactions(medicine_names):
    """
    Check for interactions using OpenFDA drug label API.
    Searches each medicine's label for mentions of other medicines
    in the interactions section.
    """
    interactions = []
    not_found = []

    # Check each pair of medicines
    for i in range(len(medicine_names)):
        for j in range(i + 1, len(medicine_names)):
            med1 = medicine_names[i]
            med2 = medicine_names[j]

            result = check_pair(med1, med2)
            if result:
                interactions.append(result)

    return interactions, not_found


def check_pair(med1, med2):
    """
    Check if med2 is mentioned in med1's drug interaction warnings.
    Uses OpenFDA drug label API.
    """
    url = "https://api.fda.gov/drug/label.json"
    
    # Search for med1's label that mentions med2 in interactions
    query = f'drug_interactions:"{med2}" AND openfda.brand_name:"{med1}"'
    params = {
        "search": query,
        "limit": 1
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("results"):
                result = data["results"][0]
                interaction_text = result.get("drug_interactions", [""])[0]
                
                # Trim to relevant portion
                if len(interaction_text) > 300:
                    interaction_text = interaction_text[:300] + "..."

                return {
                    "med1": med1,
                    "med2": med2,
                    "severity": "moderate",
                    "description": interaction_text
                }

        # Try reverse — search med2's label for med1
        query2 = f'drug_interactions:"{med1}" AND openfda.brand_name:"{med2}"'
        params2 = {
            "search": query2,
            "limit": 1
        }
        response2 = requests.get(url, params=params2, timeout=10)

        if response2.status_code == 200:
            data2 = response2.json()
            if data2.get("results"):
                result2 = data2["results"][0]
                interaction_text2 = result2.get("drug_interactions", [""])[0]

                if len(interaction_text2) > 300:
                    interaction_text2 = interaction_text2[:300] + "..."

                return {
                    "med1": med1,
                    "med2": med2,
                    "severity": "moderate",
                    "description": interaction_text2
                }

        return None

    except Exception as e:
        print(f"Error checking {med1} + {med2}: {e}")
        return None