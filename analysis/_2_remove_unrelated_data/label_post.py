from analysis_process.log import log
import re


def label_post(all_posts, all_labels):
    log("Labelling post", 1)
    for post in all_posts:
        post['related_to'] = []
        for label in all_labels:
            # This will make sure 'lks' would not match 'talks'
            pattern = f"(^|[^a-z]){label}([^a-z]|$)"
            if re.search(pattern, post['value']) is not None:
                if(label not in post['related_to']):
                    post['related_to'].append(label)
