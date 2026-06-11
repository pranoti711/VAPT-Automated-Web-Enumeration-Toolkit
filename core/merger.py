
from __future__ import annotations

import json

from pathlib import Path
from typing import Any, Dict, List


class Merger:
    """
    Central merging engine.

    Responsibilities:
    -----------------
    - Merge tool outputs
    - Merge subdomains
    - Merge URLs
    - Merge parameters
    - Merge directories
    - Merge findings
    - Merge parser outputs
    - Merge files
    """
    def unique(
        self,
        items: List[Any],
    ) -> List[Any]:

        return sorted(
            set(items)
        )

    def merge_lists(
        self,
        *lists: List[Any],
    ) -> List[Any]:

        merged = []

        for item_list in lists:

            if not item_list:
                continue

            merged.extend(item_list)

        return self.unique(merged)


    def merge_subdomains(
        self,
        *lists: List[str],
    ) -> List[str]:

        return self.merge_lists(*lists)

    def merge_urls(
        self,
        *lists: List[str],
    ) -> List[str]:

        return self.merge_lists(*lists)

    def merge_parameters(
        self,
        *lists: List[str],
    ) -> List[str]:

        return self.merge_lists(*lists)



    def merge_directories(
        self,
        *lists: List[str],
    ) -> List[str]:

        return self.merge_lists(*lists)

    def merge_files(
        self,
        files: List[str | Path],
    ) -> List[str]:

        results = []

        for file_path in files:

            try:

                file_path = Path(file_path)

                if not file_path.exists():
                    continue

                with open(
                    file_path,
                    "r",
                    encoding="utf-8",
                    errors="ignore",
                ) as f:

                    results.extend(
                        line.strip()
                        for line in f
                        if line.strip()
                    )

            except Exception:
                continue

        return self.unique(results)

    def save_merged_file(
        self,
        output_file: str | Path,
        data: List[str],
    ) -> Path:

        output_file = Path(output_file)

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            output_file,
            "w",
            encoding="utf-8",
        ) as f:

            for item in sorted(set(data)):
                f.write(f"{item}\n")

        return output_file

    def merge_dicts(
        self,
        *dicts: Dict,
    ) -> Dict:

        result = {}

        for d in dicts:

            if not isinstance(d, dict):
                continue

            for key, value in d.items():

                if key not in result:
                    result[key] = value
                    continue

                if isinstance(value, list):

                    existing = result.get(
                        key,
                        [],
                    )

                    if not isinstance(
                        existing,
                        list,
                    ):
                        existing = []

                    result[key] = self.unique(
                        existing + value
                    )

                elif isinstance(value, dict):

                    existing = result.get(
                        key,
                        {},
                    )

                    if not isinstance(
                        existing,
                        dict,
                    ):
                        existing = {}

                    existing.update(value)

                    result[key] = existing

                else:

                    result[key] = value

        return result

    def merge_findings(
        self,
        *finding_lists: List[Dict],
    ) -> List[Dict]:

        merged = []
        seen = set()

        for findings in finding_lists:

            for finding in findings:

                try:

                    key = json.dumps(
                        finding,
                        sort_keys=True,
                    )

                    if key in seen:
                        continue

                    seen.add(key)

                    merged.append(finding)

                except Exception:
                    continue

        return merged
    def merge_parser_results(
        self,
        *results: Dict,
    ) -> Dict:

        final = {

            "subdomains": [],
            "urls": [],
            "parameters": [],
            "directories": [],
            "js_files": [],
            "emails": [],
            "technologies": [],
            "sensitive_files": [],
            "api_endpoints": [],
            "findings": [],
        }

        for result in results:

            if not result:
                continue

            for key in final.keys():

                value = result.get(
                    key,
                    [],
                )

                if isinstance(
                    value,
                    list,
                ):
                    final[key].extend(value)

        for key in final:

            if key == "findings":
                continue

            final[key] = self.unique(
                final[key]
            )

        return final


    def merge_tool_outputs(
        self,
        outputs: Dict[str, List[str]],
    ) -> List[str]:

        merged = []

        for tool_output in outputs.values():

            if not tool_output:
                continue

            merged.extend(tool_output)

        return self.unique(merged)


merger = Merger()