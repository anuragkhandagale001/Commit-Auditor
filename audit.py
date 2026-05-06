import os
from git import Repo

def detect_fake_commits():
    # Update this to your target repository folder name
    repo_path = os.path.join(os.getcwd(), "GO-GREEN") 
    
    try:
        repo = Repo(repo_path)
        print(f"--- 🔍 STARTING DEEP AUDIT: {os.path.basename(repo_path)} ---\n")
        
        total_commits = 0
        fake_commits = 0
        
        # Iterate through all commits in the current branch
        for commit in repo.iter_commits():
            total_commits += 1
            
            # Authored = Date claimed by user
            # Committed = Date recorded by the system
            auth_date = commit.authored_datetime
            comm_date = commit.committed_datetime
            
            # Calculate absolute difference in seconds
            diff_seconds = abs((comm_date - auth_date).total_seconds())

            # Threshold: 1 hour (3600 seconds)
            if diff_seconds > 3600:
                fake_commits += 1
                print(f"[🚩 FLAG] {commit.hexsha[:8]} | Gap: {diff_seconds/3600:.1f} hrs | Msg: {commit.message.strip()[:30]}...")

        # Calculate Fraud Score
        fraud_score = (fake_commits / total_commits) * 100 if total_commits > 0 else 0
        
        print("\n" + "="*40)
        print(f"📊 FINAL AUDIT REPORT")
        print(f"="*40)
        print(f"Total Commits Scanned: {total_commits}")
        print(f"Suspicious Commits:    {fake_commits}")
        print(f"Fraud Score:           {fraud_score:.2f}%")
        
        print("-" * 40)
        if fraud_score > 75:
            print("VERDICT: 🚨 HIGHLY FRAUDULENT (Bot Detected)")
        elif fraud_score > 10:
            print("VERDICT: ⚠️ SUSPICIOUS (Manual Manipulation)")
        else:
            print("VERDICT: ✅ LEGITIMATE REPOSITORY")
        print("="*40)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    detect_fake_commits()
