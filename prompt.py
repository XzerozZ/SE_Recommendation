
def get_prompt(similar_houses_text, nh_name, selected_province, selected_price):
    system_prompt = f"""
    You are an AI specialized in recommending nursing homes.
    Here are some similar nursing homes based on the user's interest:
    {similar_houses_text}
    """


    user_prompt = f"""You must recommend 3 nursing homes based on the user's interest.
    You must provide a short response containing only an array of nursing home names.
    It is extremely important that the names match exactly, including every character and spacing.
    Do not recommend the following nursing home: {nh_name} because it has already been viewed by the user. This nursing home has the following details:
    - Address: {selected_province} more important than price x1.5 because the user's preference is for a location within a specific region or proximity to their home for convenience, accessibility, and familiarity. 
    - Price: {selected_price} important x1
    Instead, please recommend other nursing homes based on the address and price of {nh_name}.
    Do **not** respond in JSON or any code block format. Only provide the response as plain text without any additional formatting.
    Example response: [Home_Name_1, Home_Name_2, Home_Name_3]"""

    return system_prompt,user_prompt