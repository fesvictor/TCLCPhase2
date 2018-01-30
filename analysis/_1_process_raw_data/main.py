import os
from analysis.log import log
from analysis.save_posts import save_posts
from analysis._1_process_raw_data.parse_blog import parse_blog
from analysis._1_process_raw_data.parse_facebook import parse_facebook
from analysis._1_process_raw_data.parse_jbtalks import parse_jbtalks
from analysis._1_process_raw_data.parse_lowyat import parse_lowyat
from analysis._1_process_raw_data.parse_twitter import parse_twitter
from analysis._1_process_raw_data.parse_carinet import parse_carinet


def main(jobs, language):
    posts = []
    log(f"Parsing {language} posts", 1)
    for job in jobs:
        posts += job.run()
    save_posts(posts, f'analysis/_1_process_raw_data/output/{language}.json')
    log(f"Number of {language} posts created : " + str(len(posts)), 1)


class Job():
    def __init__(self, directory, parser):
        self.parser = parser
        self.directory = directory

    def run(self):
        return self.parse_files_from(self.directory, self.parser)

    def parse_files_from(self, directory, parser):
        log("Parsing files from " + directory, 2)
        posts = []
        for file in os.listdir(directory):
            if not file.endswith('.csv'):
                continue
            posts += parser(directory + file)
        return posts


PARENT_DIR = 'scrape-results/'
BLOG_DIR = PARENT_DIR + 'blog/'
FACEBOOK_DIR = PARENT_DIR + 'facebook/'
TWITTER_DIR = PARENT_DIR + 'twitter/'
LOWYAT_DIR = PARENT_DIR + 'forum/lowyat/'
CARINET_DIR = PARENT_DIR + 'forum/carinet/'
JBTALKS_DIR = PARENT_DIR + 'forum/jbtalks/'
MALAYSIA_KINI_DIR = PARENT_DIR + 'news/malaysiakini'

ENGLISH_JOBS = [
    Job(BLOG_DIR, parse_blog),
    Job(FACEBOOK_DIR, parse_facebook),
    Job(LOWYAT_DIR, parse_lowyat),
    Job(TWITTER_DIR, parse_twitter)
]

CHINESE_JOBS = [
    Job(JBTALKS_DIR, parse_jbtalks),
    Job(CARINET_DIR, parse_carinet) 
]

main(ENGLISH_JOBS, 'english')
main(CHINESE_JOBS, 'chinese')
