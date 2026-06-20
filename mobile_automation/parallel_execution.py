import logging
import threading

@staticmethod
def driver_runner_raise_assertion(function: callable, drivers: list, function_name: str, *args, **kwargs) -> None:

   exceptions = []

   def run_and_catch(driver):
       try:
           function(driver, *args, **kwargs)
       except Exception as e:
           exceptions.append(e)

   threads = [
       threading.Thread(target=run_and_catch, args=(driver,))
       for driver in drivers
   ]

   for thread in threads:
       thread.start()
   for thread in threads:
       thread.join()

   if exceptions:
       # raise the first one for test failure
       raise exceptions[0]
