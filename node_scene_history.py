import node_scene
DEBUG = True

class SceneHistory():
    def __init__(self, scene:'node_scene.Scene'):
        self.scene = scene
        
        self.history_stack = []
        self.history_current_step = -1
        self.history_limit = 8
        
    ##################
    def undo(self):
        if DEBUG: print('UNDO')
        if self.history_current_step > 0:
            self.history_current_step -= 1
            self.restoreHistory()

    ##################
    def redo(self):
        if DEBUG: print('REDO')
        if self.history_current_step+1 < len(self.history_stack):
            self.history_current_step += 1
            self.restoreHistory()

    ##################
    def restoreHistory(self):
        if DEBUG: 
            print('Restoring history ... current step: {0} ({1})'.format(
                self.history_current_step, len(self.history_stack)))
        self.restoreHistoryStamp(self.history_stack[self.history_current_step])

    ##################
    def storeHistory(self, desc:str):
        if DEBUG: 
            print('Storing history "{2}" ... current step: {0} ({1})'.format(
                self.history_current_step, len(self.history_stack), desc))
    
        # if pointer is not at the end
        if self.history_current_step+1 < len(self.history_stack):
            self.history_stack = self.history_stack[0:self.history_current_step+1]
        
        if self.history_current_step +1 >= self.history_limit:
            self.history_stack = self.history_stack[1:]
            self.history_current_step -= 1
        hs = self.createHistoryStamp(desc)
        self.history_stack.append(hs)
        self.history_current_step += 1
        if DEBUG: print(' -- setting step to', self.history_current_step)

    ##################
    def createHistoryStamp(self, desc:str):
        return desc
        
    ##################
    def restoreHistoryStamp(self, history_stamp):
        if DEBUG: print('HS:', history_stamp)