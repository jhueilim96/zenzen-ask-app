from app.agents import agent_executor

input_ = {'input':'please tell a movie related to naruto'}

# res = agent_executor.invoke(input_)
res_stream = agent_executor.stream(input_)
steps = [step for step in res_stream]
print(0)