
def get_prompt(similar_houses_text, nh_name, selected_address, selected_price):
    system_prompt = f"""
        You are an AI specialized in recommending nursing homes.
        Here are some similar nursing homes based on the user's interest:
        {similar_houses_text}
        """


    user_prompt = f"""You must recommend 3 nursing homes based on the user's interest.
    You must provide a short response containing only an array of nursing home names.
    It is extremely important that the names match exactly, including every character and spacing.
    Do not recommend the following nursing home: {nh_name} because it has already been viewed by the user. This nursing home has the following details:
    - Address: {selected_address}
    - Price: {selected_price}
    Instead, please recommend other nursing homes based on the address and price of {nh_name}.
    Example response: [Home_Name_1, Home_Name_2, Home_Name_3]"""

    return system_prompt,user_prompt