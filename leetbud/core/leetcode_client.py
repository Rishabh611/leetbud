"""
LeetCode API client for fetching problem information.
"""
import requests
from typing import Optional, Dict, Any
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    """HTML Parser for stripping HTML tags."""
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []

    def handle_data(self, d):
        self.text.append(d)

    def get_data(self):
        return ''.join(self.text)

class LeetCodeClient:
    """Client for interacting with LeetCode's API."""
    
    def __init__(self):
        self.base_url = "https://leetcode.com/api"
        self.graphql_url = "https://leetcode.com/graphql"
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "LeetBud"
        }

    def get_problem(self, query: str) -> Optional[Dict[str, Any]]:
        """Get problem details by query (ID or name)."""
        try:
            if query.isdigit():
                matches = self.search_problem(query)
                if matches:
                    for match in matches:
                        if str(match["id"]) == query:
                            return self.get_problem_by_slug(match["slug"])
            
            # Try direct slug first
            slug = query.lower().replace(" ", "-")
            problem = self.get_problem_by_slug(slug)
            if problem:
                return problem

            # Fall back to search
            matches = self.search_problem(query)
            if matches:
                return self.get_problem_by_slug(matches[0]["slug"])

            return None
            
        except Exception as e:
            raise RuntimeError(f"Error fetching problem: {str(e)}")

    def get_problem_by_slug(self, title_slug: str) -> Optional[Dict[str, Any]]:
        """Get problem details by title slug."""
        query = """
        query getQuestionDetail($titleSlug: String!) {
          question(titleSlug: $titleSlug) {
            questionId
            title
            difficulty
            content
            exampleTestcases
            topicTags {
              name
            }
          }
        }
        """

        try:
            response = requests.post(
                self.graphql_url,
                headers=self.headers,
                json={
                    "query": query,
                    "variables": {"titleSlug": title_slug}
                }
            )

            response.raise_for_status()
            data = response.json()

            if "errors" in data:
                raise ValueError(data["errors"][0]["message"])
            
            if not data.get("data") or not data["data"].get("question"):
                return None

            question = data["data"]["question"]
            
            return {
                "id": question["questionId"],
                "title": question["title"],
                "difficulty": question["difficulty"],
                "description": self._strip_tags(question["content"]),
                "test_cases": question["exampleTestcases"],
                "topics": [tag["name"] for tag in question["topicTags"]]
            }
            
        except requests.RequestException as e:
            raise RuntimeError(f"Network error: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Error processing problem data: {str(e)}")

    def search_problem(self, query: str) -> list:
        """Search for problems matching the query."""
        try:
            response = requests.get(f"{self.base_url}/problems/all", headers=self.headers)
            response.raise_for_status()
            data = response.json()

            query = query.lower()
            matches = []

            for problem in data.get("stat_status_pairs", []):
                stat = problem.get("stat", {})
                title = stat.get("question__title", "").lower()
                title_slug = stat.get("question__title_slug", "")
                question_id = stat.get("frontend_question_id", "")

                if query in title or \
                   query in title_slug or \
                   (query.isdigit() and question_id == int(query)):
                    matches.append({
                        "id": question_id,
                        "title": title,
                        "slug": title_slug,
                        "difficulty": ["Easy", "Medium", "Hard"][problem.get("difficulty", {}).get("level", 1) - 1]
                    })

            matches.sort(key=lambda x: (0 if str(x["id"]) == query or x["slug"] == query else 1, x["id"]))
            return matches
            
        except requests.RequestException as e:
            raise RuntimeError(f"Network error: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Error searching problems: {str(e)}")

    @staticmethod
    def _strip_tags(html: str) -> str:
        """Remove HTML tags from text."""
        s = MLStripper()
        s.feed(html)
        return s.get_data() 