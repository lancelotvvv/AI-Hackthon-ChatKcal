
# %%
import streamlit as st
import os
from tabulate import tabulate
import json
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
import pandas as pd
# from langchain.memory import ConversationBufferMemory
os.environ['OPENAI_API_KEY'] = "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"

st.title('''⭐🍇🍉🍍ChatKcal🥭🍎🥝⭐
          🍽️ 🌿Your Personal AI Nutritionist Assitant
          ''')


# openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')
def generate_response(age_text, weight_text, height_text, activity_level, plan_type):
    llm = OpenAI(temperature=0, max_tokens=2000)
    # Notice that "chat_history" is present in the prompt template
    template = """You are to create a meal plan

            Previous conversation:
            {chat_history}

            New human question: {question}
            Response:"""
    prompt = PromptTemplate.from_template(template)
    # Notice that we need to align the `memory_key`
    # To not return the entire history, set verbose=False
    memory = ConversationBufferMemory(memory_key="chat_history")

    answer_format = '''
            {
                "reply": "",
                "menu": {
                    "Breakfast": [
                        {
                            "Dish": "dish name",
                            "Ingredients": [
                                ["ingredients_name", "quantity", "calories"],
                                ["ingredients_name", "quantity", "calories"]
                            ],
                            "Total_calories": ""
                        }
                    ],
                    .....
                }
            }
            '''

    reply = '''
            {
                "reply": "I understand",
                "menu": {
                    "Breakfast": [],
                    "Lunch":[],
                    "Dinner":[]
                }
            }
            '''
    memory.save_context({"input": "All your responses should only be in a json file like the following, "
                                  "put your response into the reply section. the menu secotion should be a meal plan"
                                  "with the calories calculation :\n" + answer_format +
                                  " respond I understand if you understand"},
                        {"output": reply})
    conversation = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=True,
        memory=memory
    )
    answer = conversation(f'''
            Questions:
            For a person: weight of {weight_text}kg, age of {age_text} years old, height of {height_text}cm and {activity_level} Level. 
            please design a detailed {plan_type} including calories breakdown for this person.
            ''')




    sample_reply = json.loads(answer["text"])

    # # Initialize empty lists to store the data
    # rows = []
    #
    # # Loop through the menu items and their details
    #
    # for meal, dishes in sample_reply['menu'].items():
    #     for dish in dishes:
    #         ingredients_list = ", ".join([ingredient[0] for ingredient in dish['Ingredients']])
    #         total_calories_range = dish['Total_calories']
    #         rows.append([meal, dish['Dish'], ingredients_list, total_calories_range])
    #
    # # Create a DataFrame
    # df = pd.DataFrame(rows, columns=['Meal', 'Dish', 'Ingredients', 'Total_calories'])
    # st.table(df)

    for meal, dishes in sample_reply["menu"].items():
        st.text(meal)

        table_data = []
        for item in dishes:
            dish = item["Dish"]
            total_calories = item["Total_calories"]
            ingredients = "\n".join([f"{ing[0]} ({ing[1]}) - {ing[2]}" for ing in item["Ingredients"]])
            table_data.append([dish, ingredients, total_calories])

        # Create a card-like display
        table = tabulate(table_data, headers=["Dish", "Ingredients", "Total Calories"], tablefmt="grid")

        # Print the card-like display
        st.text(table)


with st.form('my_form'):
    # gender_text = st.text_area(('Enter your gender in male/female:', 'male'))
    age_text = st.slider('How old are you?', 0, 130, 25)
    weight_text = st.slider("What's your weight in kg?", 0, 200, 60)
    height_text = st.slider("What's your height in cm?", 0, 300, 165)
    col1, col2 = st.columns(2)
    with col1:
        activity_level = st.radio(
            "What is your Daily Activity Level 🤸",
            key="activity",
            options=['Light Activity', 'Moderate Activity', 'Vigorous Activity'],
        )
    with col2:
        plan_type = st.radio(
            "What do you need 🍔",
            key="plan",
            options=['Daily Meal Plan', 'Nutrition Plan'],
        )

    # activity_level = st.selectbox(
    # 'What is your Daily Activity Level',
    # ('Light Activity', 'Moderate Activity', 'Vigorous Activity'))

    # activity_level = st.radio(
    #     "What is your Daily Activity Level 👉",
    #     key="activity",
    #     options=['Light Activity', 'Moderate Activity', 'Vigorous Activity'],
    # )
    # plan_type = st.radio(
    #     "What do you need 👉",
    #     key="plan",
    #     options=['Nutrition Plan', 'Daily Meal Plan'],
    # )
    submitted = st.form_submit_button('Generate your plan')
    if age_text == '':
        st.warning('Please choose your age', icon='⚠')
    elif weight_text == '':
        st.warning('Please choose your weight', icon='⚠')
    elif height_text == '':
        st.warning('Please choose your height', icon='⚠')
    elif activity_level == '':
        st.warning('Please choose your activity level', icon='⚠')
    elif plan_type == '':
        st.warning('Please choose your plan type', icon='⚠')
    elif submitted and os.environ['OPENAI_API_KEY'].startswith('sk-'):
        # template = '''
        # Questions:
        # Calculate Daily calorie intake by using
        # Equation 1: Basal Metabolic Rate (BMR) = 10 x Weight (kg) + 6.25 x Height (cm) - 5 x Age (years) + 5,
        # and Equation 2: Daily calorie intake = BMR x Activity Level
        # Based on 2023 nutriention table and daily calorie intake result from previous step,
        # please create a nutrition plan for a person with following infomation:
        # weight of {weight_text}kg, age of {age_text} years old, height of {height_text}cm and {activity_level} Level.
        # Only return the final detailed meal plan in a table format, break down into calories, make sure starting with my weight and age and my colaries intake
        # '''

        # template = '''
        # Questions:
        # Calculate Daily calorie intake by using
        # Equation 1: Basal Metabolic Rate (BMR) = 10 x Weight (kg) + 6.25 x Height (cm) - 5 x Age (years) + 5,
        # and Equation 2: Daily calorie intake = BMR x Activity Level
        # Based on 2023 nutriention table and daily calorie intake result from previous step,
        # please create a nutrition plan for a person with following infomation:
        # weight of {weight_text}kg, age of {age_text} years old, height of {height_text}cm and {activity_level} Level.
        # Only return the final detailed meal plan in a table format, break down into calories, make sure starting with my weight and age and my colaries intake
        # Answer: Let's think step by step.
        # '''

        generate_response(age_text, weight_text, height_text, activity_level, plan_type)
