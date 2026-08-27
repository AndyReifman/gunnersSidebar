#!/usr/bin/python3


from sidebar.injury.update import updateSidebar
from sidebar.results.update import updateResults
from sidebar.table.update import updateSidebar as update_table

# subprocess.call(
#     [os.path.join(os.path.dirname(os.path.abspath(__file__)), "injury/update.py")]
# )
# subprocess.call(
#     [os.path.join(os.path.dirname(os.path.abspath(__file__)), "results/update.py")]
# )
# subprocess.call(
#     [os.path.join(os.path.dirname(os.path.abspath(__file__)), "table/update.py")]
# )
# subprocess.call(
#     [os.path.join(os.path.dirname(os.path.abspath(__file__)), "statistics/update.py")]
# )


def main():
    try:
        updateSidebar()
    except:
        pass
    try:
        updateResults()
    except ValueError:
        pass
    try:
        update_table()
    except:
        pass
    # try:
    #     updateGoals()
    # except AttributeError:
    #     pass


if __name__ == "__main__":
    main()
