from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool


student_db = {
    "24BAI0149" : {"Name": "Sithi Vignesh", "ID": "24BAI0149", "Branch": "CSE AI/ML", "Year of Passing": 2028},
    "24BAI0141" : {"Name": "Nithin Balaji", "ID": "24BAI0141", "Branch": "CSE AI/ML", "Year of Passing": 2028},
    "24BAI0110" : {"Name": "Logith Aadhithiya", "ID": "24BAI0110", "Branch": "CSE AI/ML", "Year of Passing": 2028},
    "24BDS0345" : {"Name": "Harshath", "ID": "24BDS0345", "Branch": "CSE Data Science", "Year of Passing": 2028}
}

@tool
def libraryFineCalculator(days: int) -> int:
    '''Calculates the fine amount for returning a library book late. input is the number of delay days'''
    fine = 5 * days
    return fine

@tool
def feeBalance(total: int, paid: int) -> int:
    '''Calculates the fee balance to be paid. input is total fee and the already paid amount'''
    pending = total - paid
    return pending

@tool
def hostelFeeCalculator(fee: int, months: int) -> int:
    '''Calculates the hostel fee. the input is the fee per month and the number of months'''
    payment = fee * months
    return payment

@tool
def attendenceCalculator(total: int, attended: int) -> dict:
    '''Calculates the attendance percetage and the exam eligibity based on that. the input is total classes and the attended classes'''
    percentage = (attended/total) * 100
    if percentage < 75 : eligibility = False
    else : eligibility = True
    ans = {"percentage":percentage, "eligibility":eligibility}
    return ans

@tool
def resultCalculator(a: int,b: int,c: int,d: int,e: int) -> dict:
    '''Calculates the average marks, grade and pass/fail status bases on the the marks. the input is the marks of the 5 subjects'''
    avg = (a+b+c+d+e)/5
    if avg >= 90 : grade = "A"
    elif avg >= 75 and avg < 90 : grade = "B"
    elif avg >= 60 and avg < 75 : grade = "C"
    else : grade = "D"
    if avg >=50 : status = True
    else : status = False
    ans = {"average":avg, "grade":grade, "status":status}
    return ans

@tool
def studentInformationFinder(student_id: str) -> str:
    '''Retreives the student's information based on the student ID. the input will be the student ID'''
    if student_id in student_db:
        student  = student_db[student_id]
        ans = f"Name: {student['Name']}, ID: {student['ID']}, Branch: {student['Branch']}, Year of Passing: {student['Year of Passing']}"
        return ans
    else : return ("Student info not in Database")


llm = ChatOllama(model = "qwen2.5:3b")

tools = [libraryFineCalculator,feeBalance,hostelFeeCalculator,attendenceCalculator,resultCalculator,studentInformationFinder]

agent = create_react_agent(llm, tools)

print("\n----------------------------------------------------")
print("Heloo, Welcome to Smart College Assitant!")
print("Press Ctrl + C or type 'Stop' to end the Chat")
print("----------------------------------------------------\n")
while True:
    user_input = input("You: ")
    if user_input.lower() == "stop" : break
    response = agent.invoke({"messages": [("human", user_input)]})
    print("AI: " + response["messages"][-1].content + "\n")