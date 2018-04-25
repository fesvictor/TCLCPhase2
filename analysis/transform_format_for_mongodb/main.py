from analysis.libs.load_posts import load_posts
from analysis.libs.save_posts import save_posts
from analysis.transform_format_for_mongodb.tokenize_post_into_sentence import tokenize_post_into_sentence
import re

GENERATE_SAMPLE = False


def main(language):
    post_id = 0
    tokenized_posts = []
    posts = load_posts(f'analysis/_2_remove_unrelated_data/{language}.json')
    for p in posts:
        p["belongs_to"] = "p" + str(post_id)
        post_id += 1
        p["semantic_value"] = "unassigned"
        p["value"] = re.sub(r'^https?:\/\/.*[\r\n]*', '',  p["value"], flags=re.MULTILINE)
        p["value"] = re.sub(r'\{[^}]*\}', ' ', p["value"])
        sentences= tokenize_post_into_sentence(p["value"])
        for s in sentences:
            copy= p.copy()
            copy["value"]= s
            tokenized_posts.append(copy)

    if GENERATE_SAMPLE:
        save_posts(tokenized_posts[:100],
                f'analysis/transform_format_for_mongodb/{language}_sample.json')
    save_posts(tokenized_posts,
               f'analysis/transform_format_for_mongodb/{language}.json')


main('english')
main('chinese')
