import os
import streamlit as st
from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain
# from langchain.memory import ConversationBufferMemory

my_api_key_yunfei = "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"
os.environ['OPENAI_API_KEY'] = my_api_key_yunfei

st.title('''⭐🍇🍉🍍ChatKcal🥭🍎🥝⭐
          🍽️ 🌿Your Personal AI Nutritionist Assitant
          ''')

# openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')
def generate_response(prompt,age_text,weight_text,height_text,activity_level,plan_type):
    llm = OpenAI(temperature=0,max_tokens=2000)
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    # st.info(llm(prompt.format(weight_text=weight_text,age_text=age_text)))
    st.info(llm_chain.run(weight_text=weight_text, 
                          age_text=age_text,
                          height_text=height_text,
                          activity_level=activity_level,
                          plan_type=plan_type))


with st.form('my_form'):
    # gender_text = st.text_area(('Enter your gender in male/female:', 'male'))
    age_text = st.slider('How old are you?', 0, 130, 25)
    weight_text = st.slider("What's your weight in kg?", 0, 200, 60)
    height_text = st.slider("What's your height in cm?", 0, 300, 165)
    col1, col2= st.columns(2)
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
    if  age_text=='':
        st.warning('Please choose your age', icon='⚠')
    elif  weight_text=='':
        st.warning('Please choose your weight', icon='⚠')
    elif  height_text=='':
        st.warning('Please choose your height', icon='⚠')
    elif  activity_level=='':
        st.warning('Please choose your activity level', icon='⚠')
    elif  plan_type=='':
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

        template = '''
        Questions:
        For a person: weight of {weight_text}kg, age of {age_text} years old, height of {height_text}cm and {activity_level} Level. 
        Step 1: Calculate BMR using Equation 1: Basal Metabolic Rate (BMR) = 10 x Weight (kg) + 6.25 x Height (cm) - 5 x Age (years) + 5
        Step 2: Calculate Daily Calorie Intake using BMR from step 1 and Equation 2: Daily calorie intake = BMR x Activity Level
        Step 3: Based on 2023 nutriention table and daily calorie intake result from previous step, 
        Answer: Let's think step by step.
        please design a detailed {plan_type} including calories breakdown for this person.
        '''

        prompt = PromptTemplate(template=template, input_variables=['age_text','weight_text','height_text','activity_level','plan_type'])
        # print(prompt)
        generate_response(prompt,age_text,weight_text,height_text,activity_level,plan_type)