from github import Github
from datetime import timedelta
import csv


def main():
    output = open("pr_scrape.csv", "w")
    writer = None
    token = input("Github access token: ")
    first_created, last_created = (None, None)

    g = Github(token)
    r = g.get_repo("zapier/zapier")
    pulls = r.get_pulls(state="closed")

    for pr in pulls:
        if pr.user.login.startswith("zapzap"):
            print("Skipping {}".format(pr.title))
            continue
        if not pr.is_merged():
            print("Skipping unmerged: {}".format(pr.title))
            continue
        if first_created is None:
            first_created = pr.created_at
            last_created = pr.created_at - timedelta(days=30)
        if pr.created_at < last_created:
            print("Returning, since we've analysed 30 days of PRs")
            return
        print("Processing: {}".format(pr.title))
        pr_data = get_pr_data(pr)
        if writer is None:
            writer = csv.DictWriter(output, pr_data.keys())
            writer.writeheader()
        writer.writerow(pr_data)


def get_pr_data(pr):
    reviewed_by = ""
    for review in pr.get_reviews():
        if review.state == "APPROVED":
            reviewed_by = review.user.login
    return {
        "author": pr.user.login,
        "open_seconds": (pr.closed_at - pr.created_at).total_seconds(),
        "reviewed_by": reviewed_by,
        "num_commits": pr.commits,
        "changed_files": pr.changed_files,
        "diff_size": pr.additions + pr.deletions,
    }


if __name__ == "__main__":
    main()
