class PerformanceLogger:
    def __init__(self):
        self.log_file = open('performance.log', 'w')

    def log_episode_results(self, episode_results):
        episode_time = episode_results.get('time')
        episode_gems = episode_results.get('gems')
        self.log_file.write('Episode Results | Time: ' + str(episode_time) + ' | Gems: ' + str(episode_gems) + '\n')

    def quit(self):
        self.log_file.close()
