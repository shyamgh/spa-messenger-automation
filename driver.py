import argparse
import os
from time import sleep

#-------------------------------------------
def init_app():
    print('starting hipster-messenger container...')
    os.system('docker run -d --rm -it -p3000:3000 -p5000:5000 registry.celus.co/technical-challenge/hipster-messenger:stable')
    sleep(5)

def terminate_app():
    print('stopping hipster-messenger container...')
    os.system("docker stop $(docker ps | grep hipster | awk '{print $1}')")
    sleep(2)

def main(args):
    initApp = args.initApp
    quitApp = args.quitApp
    parallelTest = args.parallelTest
    htmlReport = args.htmlReport
    captureSysLog = args.captureSysLog
    reruns = args.reruns

    # start messenger container
    if initApp:
        init_app()

    cmd = 'pytest -n {} --reruns {} --html={} --self-contained-html'.format(
        parallelTest, reruns, htmlReport)

    if captureSysLog:
        cmd = '{} {}'.format(cmd, '--capture=sys')

    # run pytest
    os.system(cmd)
    
    # stop messenger container
    if quitApp:
        terminate_app()

def open_html_report(reportFile):
    try:
        import webbrowser
        new = 2  # open in a new tab
        # open an HTML file in browser
        cwd = os.getcwd()
        url = "file://{}/{}".format(cwd, reportFile)
        webbrowser.open(url, new=new)
    except:
        pass

#-------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument(
    "--initApp", help="Set True if need to start messenger container. Default is False.", required=False, default=False, type=bool)
parser.add_argument(
    "--quitApp", help="Set True if need to stop messenger container. Default is False.", required=False, default=False, type=bool)
parser.add_argument(
    "--parallelTest", help="Number of tests to run in parallel. Default is 5.", required=False, default=5, type=int)
parser.add_argument(
    "--htmlReport", help="Set True if need to stop messenger container. Default is False.", required=False, default='report.html', type=str)
parser.add_argument(
    "--captureSysLog", help="Set False if logger logs and console logs not required in html report. Default is True.", required=False, default=True, type=bool)
parser.add_argument(
    "--reruns", help="Number of time failed tests to rerun. Default is 1.", required=False, default=1, type=int)

if __name__ == "__main__":
    args = parser.parse_args()
    os.system('mkdir -p {}/screenshots'.format(os.getcwd()))
    main(args=args)
    open_html_report(args.htmlReport)
