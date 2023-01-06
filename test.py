import subprocess

command = "docker-compose run --rm freqtrade hyperopt --config C:/ft_userdata/user_data/config.json --enable-protections --strategy SampleStrategy --hyperopt-loss SharpeHyperOptLoss -i 5m -e 10"


subprocess.run(command, shell=True)


# def restart_freqtrade():
#     """
#     Command, that restart working docker-compose
#     :return:
#     """
#     print("start restart")
#     subprocess.run(["docker-compose", "restart", "freqtrade"])
#     print("finish restart")
#
#
# restart_freqtrade()