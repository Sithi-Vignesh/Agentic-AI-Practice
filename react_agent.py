import ollama

def get_weather(location):
    weather_report = {
        "chennai": "heavy Rain",
        "bangalore": "Super Cold"
    }
    if location in weather_report:
        loc  = weather_report[location]
        return loc
    else : return ("location info not in Database")

def get_game_price(game):
    game_report = {
        "elden ring": "4,999/-",
        "expedition 33": "2,499/-"
    }
    if game in game_report:
        return game_report[game]
    else : return ("game info not in Database")


tool_router = {
    "get_weather": get_weather,
    "get_game_price": get_game_price
}
def checkTool(tool_name):
    if tool_name in tool_router: return True
    else : return False

system_prompt = '''You are a helper AI who have the Data of locations and Games. but you must follow a set of steps before giving the answer,
- NEVER CHANGE THE FORMAT. AND ALWAYS WAIT FOR THE TOOL TO RETURN THE ANSWER. NEVER CREATE YOUR OWN ANSWER.
- you must think what you are gonna do A.K.A THOUGHT, format -> "THOUGHT: i need X to perform this task" x is one of the available tools
- you must use the THOUGHT to perform the ACTION with the tools, format example-> "ACTION: get_weather(chennai)"
- After writing ACTION, stop immediately. Do not write OBSERVATION yourself.
- only write FINAL ANSWER when you have gathered all required information.
- after using the tools, if u get the final answer then you must return the answer in this way,format-> "FINAL ANSWER:..."
- but if u still didnt reach the final answer then u must again repeat the THOUGHT, ACT and OBSERVE process, format-> "OBSERVATION: <what tool retuned>"
- tools available are: get_weather,use this to get the weather of a location, the input string is the location and the output string is the weather
- next tool is get_game_price,use this to get the price of the game, the input string is the game name and the output string is the game price'''

context_window = [
    {"role":"system", "content":system_prompt}
]

while True:
    user_input = input("You: ")
    context_window.append({"role":"user", "content": user_input})
    while True:
        response = ollama.chat(model="qwen2.5:3b", messages=context_window)
        llm_output = response["message"]["content"]
        print(llm_output)
        context_window.append({"role":"assistant" ,"content":llm_output})

        if "ACTION" in llm_output.upper():
            llmoutput = llm_output[10:-1]
            x = llm_output.split("\n")
            for y in x:
                if y.startswith("ACTION:"):
                    z = y.split("(")
                    tool = z[0].split()[1]
                    arg = z[1][:-1].strip('"')
                    print(arg)
                    if checkTool(tool):
                        result = tool_router[tool](arg.lower())
                        context_window.append({"role":"user", "content": result})
        if "FINAL ANSWER" in llm_output.upper():
            break

    if "FINAL ANSWER" in llm_output.upper():
        break
