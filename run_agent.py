from agent import IOTAgent 
if __name__ == "__main__":
    agent = IOTAgent("data/sensors.csv")
    while True:
        question = input("\n Ask IOT Agent: ")
        answer = agent.run(question)
        print("\n Final Answer:\n", answer)

    