from actor_bot import Actor_bot
import time


class Film_scene:
    def __init__(self, script, room):
        self.script = script
        self.room = room
        self.actors_names = []
        self.actors = []
        self.lines_all_actors = []
    
    def hire_actors(self):
        script = open("chatbot/movie_dialogue/" + self.script + ".tsv", "r")
    
        for line in script:
            line = line.split("\t")
            actor_name = line[3]
            if actor_name not in self.actors_names:
                self.actors_names.append(actor_name)
                actor = Actor_bot(actor_name)
                actor.enter_chatroom(self.room)
                self.actors.append(actor)
      

    def act_out_the_scene(self):
        line_number = 0
        script = open("chatbot/movie_dialogue/" + self.script + ".tsv", "r")
        script_list = []

        for line in script:
            script_list.append(line)

        last_line = False
    
        for line in script_list:
            line = line.split("\t")
            actor_name = line[3]
            line_speach = line[4]
            line_number += 1
            time.sleep(2)
            if line_number == len(script_list):
                last_line = True

            for actor in self.actors:
                if actor.name == actor_name:
                    actor.read_line(line_speach, last_line)
                
        
        for actor in self.actors:
            actor.end_scene()





film1 = Film_scene("short", "7")
film1.hire_actors()
film1.act_out_the_scene()

        