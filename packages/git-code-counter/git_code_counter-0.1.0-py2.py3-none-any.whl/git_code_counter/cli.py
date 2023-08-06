# -*- coding: utf-8 -*-

"""Console script for git_code_counter."""
import sys
import click
import git
import subprocess
import json
import shutil
import matplotlib.pyplot as plt  # type: ignore
from matplotlib.dates import date2num
from matplotlib.dates import DateFormatter
import datetime

@click.command()
@click.argument('url')
@click.option('--local/--remote', default=False, help='Use local if use local repo.')
@click.option('--workspace', default='./repo', help='Clone in workspace.')
@click.option('--branch', default='master', help='Branch name.')
@click.option('--count', default='20', help='Max commit count to iterate.')
@click.option('--lang-limit', default='5', help='Max language count to show.')
def main(url, local, workspace, branch, count, lang_limit):
  lang_limit = int(lang_limit)

  if local:
    repo = git.Repo(url)
  else:
    repo = git.Repo.clone_from(url, workspace)
  try:
    hexsha_list = []
    commit_time_list = []
    analysis_list = []
    langs = {}
    repo.git.checkout(branch)
    for item in repo.iter_commits(branch, max_count=count):
      hexsha_list.append(item.hexsha)
      commit_time_list.append(item.committed_date)

    for cnt, hexsha in enumerate(hexsha_list):
      click.echo("Checkout {0}".format(hexsha))
      repo.git.checkout(hexsha) #, b='tmp{0}'.format(cnt))

      process = subprocess.Popen(
          ['cloc', '--exclude-dir=target,vendor,node_modules,build', '--json', workspace],
          stdout=subprocess.PIPE,
          stderr=subprocess.PIPE,
      )

      out, _ = process.communicate()
      if process.returncode != 0:
          click.echo('Failed to count the lines of code for {}!'.format(workspace), err=True)
          exit(1)

      stats = json.loads(out)
      stats.pop('header', None)
      stats.pop('SUM', None)

      loc = {}
      for key, value in stats.items():
        loc[key] = {'lines': value['code'] }
        if not key in langs:
          langs[key] = 0
        langs[key] += value['code']
      stats = {
          'name': '',
          'loc': loc,
          'sum': sum(v['code'] for v in stats.values()),
      }
      analysis_list.append(stats)

    sorted_langs = sorted(langs.items(), key=lambda x:x[1])
    sorted_langs = sorted_langs[-lang_limit: len(sorted_langs)]
    fig = plt.figure(figsize=(3, 3), dpi=300)
    ax = fig.add_subplot(1, 1, 1)
    x_values = date2num([datetime.datetime.fromtimestamp(unix_time) for unix_time in commit_time_list])

    legend_1 = []
    legend_2 = []
    y_values = None
    for lang in sorted_langs:
      bottom_y_values = y_values
      y_values = [stats['loc'][lang[0]]['lines'] if lang[0] in stats['loc'] else 0 for stats in analysis_list]
      if bottom_y_values:
        bar = ax.bar(x_values, y_values, bottom=bottom_y_values)
      else:
        bar = ax.bar(x_values, y_values)
      legend_1.append(bar[0])
      legend_2.append(lang[0])
    ax.set_xlabel(r'time')
    ax.set_ylabel(r'lines')

    # ax.set_title('')
    ax.set_xlim(min(x_values), max(x_values))
    ax.xaxis.set_major_formatter(DateFormatter("%m-%d"))
    fig.tight_layout()
    plt.legend(tuple(legend_1), tuple(legend_2), loc='upper left', fontsize=5)
    plt.show()
  except ZeroDivisionError as e:
   click.echo(str(e), err=True)

  if not local:
    shutil.rmtree(workspace)

  return 0


if __name__ == "__main__":
  sys.exit(main())  # pragma: no cover
