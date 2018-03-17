from analysis.libs.load_posts import load_posts
from analysis.libs.save_posts import save_posts

def main(language):
    posts = load_posts(f'analysis/_2_remove_unrelated_data/{language}.json')
    for p in posts:
        p["semantic_value"] = "unassigned"
    save_posts(posts, f'analysis/transform_format_for_mongodb/{language}.json')

main('english')
main('chinese')