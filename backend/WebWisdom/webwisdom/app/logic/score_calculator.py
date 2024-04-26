



def find_unique_list(data, unique_key):
    """recursive function to locate the unique array that contains the vulnerability scores

    Args:
        data (list): list of any size and any child lists and dictionaries
        unique_key (string): the unique name of a list you want to retrieve from the data

    Returns:
        list[int]: list of integers
        None: if not list is found matching the unique_key then None is returned
    """

    if isinstance(data, dict):
        for key, value in data.items():
            if key == unique_key:
                return value
            elif value is not None and isinstance(value, (dict, list)):
                result = find_unique_list(value, unique_key)
                if result is not None:
                    return result

    elif isinstance(data, list):
        for item in data:
            if item is not None:
                result = find_unique_list(item, unique_key)
                if result is not None:
                    return result

    return None


def get_vulnerability_scores_from_report_and_calculate(report, ssl):
    try:
        total_risk = []
        data_total_risk = []

        total_risk.append(
            find_unique_list(report, "total_risk_mysql"))

        total_risk.append(
            find_unique_list(report, "total_risk_headers"))
        total_risk.append(find_unique_list(report, "total_risk_files"))
        total_risk.append(find_unique_list(report, "total_risk_cookies"))
        total_risk.append(find_unique_list(
            report, "total_risk_server_side_vulnerabilities"))


        if ssl is not None and ssl:
            total_risk.append([ssl])

        print("this is the", report)

        if total_risk is None:
            print("total_risk is None")
            return {"vulnerability_score": "error in calculating score"}

        if total_risk is not None:
            for list in total_risk:
                if list is not None:
                    for int in list:
                        data_total_risk.append(int)

       
        

        result = calculate_security_score_from_list(data_total_risk)
        print("vulnerability score", data_total_risk,
            "end of vulnerability score")
        
        print(result)
        return result
    except Exception as e:
        print("error in get_vulnerability_scores_from_report_and_calculate", e)
        return {"vulnerability_score": "error in calculating score"}


def calculate_security_score_from_list(data):
    """ score is calculated by mapping each vulnerability level(severity) to a pre-defined weight, these weights then subtract from the base_score.

    Args:
        data (list:int): data to calculate score with
    Raises:
        HTTPException: if data adds up to 0 a 400 exception is raised

    Returns:
        dictionary (list:int): returns a dictionary that contains the data used and the final calculated score
    """
    try:
        if data is None:
            return {"security_score_error": "data can not be none"}

       
        impact_map = {1: 0.3, 2: 0.5, 3: 0.8, 4: 1.5, 5: 3}

       
        base_score = 10

        # uses the data list contents as keys to get the corresponding impact value from the impact_map and adds it all up, if the data contains a value that is not a key inside the impact_map then 0 is added which effectively does not change the final sum
        total_impact = sum(impact_map.get(v, 0) for v in data)

        
        final_score = max(0, base_score - total_impact)
        final_score = round(final_score,1)
        
        return {"security_score": final_score, "security_score_data": data}
    except Exception as e:
        print("error in calculate_security_score_from_list: ", e)
        return {"error": "error in calculating security score"}


def add_scores_of_other_tests(test1:list,test2:list):
    """add the list of numbers that is returned from your security test here

    Args:
        test1 (list): _description_
        test2 (list): _description_
    """
    
    total_data = test1+test2
    return total_data
    

