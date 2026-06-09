from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

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


llm = ChatOllama(model = "qwen2.5:3b")

tools = [libraryFineCalculator,feeBalance,hostelFeeCalculator,attendenceCalculator,resultCalculator]

agent = create_react_agent(llm, tools)

print("----------------------------------------------------")
print("Hello, Welcome to Smart College Assitant!")
print("Press Ctrl + C or type Stop to terminate the Chat")
print("----------------------------------------------------")
while True:
    user_input = input("You: ")
    if user_input.lower() == "stop" : break
    response = agent.invoke({"messages": [("human", user_input)]})
    print("AI: " + response["messages"][-1].content)