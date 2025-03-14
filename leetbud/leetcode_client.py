import requests

class LeetCodeClient:
    def __init__(self):
        self.base_url = "https://leetcode.com/api"
        self.graphql_url = "https://leetcode.com/graphql"
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "LeetBud"
        }

    def get_problem_by_slug(self, title_slug):
        """
        Get problem by title slug
        """
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

        variables = {
            "titleSlug": title_slug
        }

        response = requests.post(
            self.graphql_url,
            headers = self.headers,
            json={
                "query": query,
                "variables": variables
            }
        )

        if response.status_code != 200:
            print(f"Error fetching problem: {response.status_code}")
            return None
        
        data = response.json()

        if "errors" in data:
            print(f"API error: {data['errors'][0]['message']}")
            return None
        
        if not data.get("data") or not data["data"].get("question"):
            print("Problem not found")
            return None

        question = data["data"]["question"]

        from html.parser import HTMLParser

        class MLStripper(HTMLParser):
            def __init__(self):
                super().__init__()
                self.reset()
                self.strict = False
                self.convert_charrefs= True
                self.text = []


            def handle_data(self, d):
                self.text.append(d)

            def get_data(self):
                return ''.join(self.text)

            
        def strip_tags(html):
            s = MLStripper()
            s.feed(html)
            return s.get_data()
        
        return {
            "id": question["questionId"],
            "title": question["title"],
            "difficulty": question["difficulty"],
            "description": strip_tags(question["content"]),
            "test_cases": question["exampleTestcases"],
            "topics": [tag["name"] for tag in question["topicTags"]]
        }


    def search_problem(self, query):
        """
        Search problem by query
        """
        url = f"{self.base_url}/problems/all"

        try:
            response = requests.get(url, headers=self.headers)
            print(response)

            if response.status_code != 200:
                return []

            data = response.json()
            stat_status_pairs = data.get("stat_status_pairs", [])

            query = query.lower()

            matches = []

            for problem in stat_status_pairs:
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
                        "difficulty": ["Easy", "Medium", "hard"][problem.get("difficulty", {}).get("level", 1) - 1]
                    })
            matches.sort(key=lambda x:(0 if str(x["id"]) == query or x["slug"] == query else 1, x["id"]))
            return matches
        except Exception as e:
            print(f"Error searching problem: {e}")
            return []

    def get_problem(self, query):
        """
        Get problem by query
        """ 

        if query.isdigit():
            matches = self.search_problem(query)
            if matches:
                for match in matches:
                    if str(match["id"]) == query:
                        return self.get_problem_by_slug(match["slug"])
        slug = query.lower().replace(" ", "-")
        problem = self.get_problem_by_slug(slug)
        if problem:
            return problem

        matches = self.search_problem(query)
        if matches:
            return self.get_problem_by_slug(matches[0]["slug"])

        return None