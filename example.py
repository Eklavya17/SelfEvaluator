import pdb

# Sample code to debug
def my_function():
    for i in range(3):
        print("Hello World")
        print(i, "this is value of i")
        print(100/0)
# Start the debugger
my_function()
# class AutoStepPdb(pdb.Pdb):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.auto_step = True

#     def interaction(self, frame, traceback):
#         # if traceback is not None:
#         #     print("Error encountered. Stopping.")
#         #     super().interaction(frame, traceback)
#         if self.auto_step:
#             self.onecmd('step')
#         else:
#             super().interaction(frame, traceback)

# if __name__ == "__main__":
#     debugger = AutoStepPdb()
#     debugger.set_trace()
#     my_function()
# my_function()
