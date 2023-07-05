# TimelineQA


TimelineQA is a benchmark for accelerating progress on querying lifelogs. TimelineQA can generate lifelogs of imaginary people. The episodes in the lifelog
range from major life episodes such as high school graduation to those that occur on a daily basis such as going for a run.

TimelineQA Reference --- [https://arxiv.org/abs/2306.01069](https://arxiv.org/abs/2306.01069):
```
@article{tan2023timelineqa,
      title={TimelineQA: A Benchmark for Question Answering over Timelines},
      author={Wang-Chiew Tan and Jane Dwivedi-Yu and Yuliang Li and Lambert Mathias and Marzieh Saeidi and Jing Nathan Yan and Alon Y. Halevy},
      journal={arXiv preprint:2306.01069},
      year={2023}
}
```

**Disclaimer**: We recognize that the lifelogs generated in this work are far from being exhaustively comprehensive. While we strived to make the lifelogs complex enough to benchmark and compare current state-of-the-art, these lifelogs would not be considered diverse in the sense that a social scientist would note, and are likely biased by the life experiences of its creators. We encourage future work in creating lifelogs that are more inclusive and faithful to all walks of life. This includes further work in making lifelogs that are more diverse in terms of life experiences, personas, and queries as well as more granular and complex in detail.

## Generating a personal timeline

```
python3 generateDB.py -h
```

```
generateDB.py -h -y <finalyear> -d <directory> -o <outputfile> -s <seed> -c <category>

-y   final year. default is 2022
-d   directory to use for outputing files
-t   template file for generating text. defaults to "templates.json" if unspecified
-v   verbose mode if specified
-o   outputfilename. defaults to default.json
-s   seed for random number generator. defaults to 12345
-c   sparse|medium|dense daily episodes
```

  
For example,
  
```
python3 generateDB.py -y 2022 -s 11111 -c "sparse" -d mydir -o sparse-example.json
```

generates a timeline of a fictatious person starting from when the person is 18 years old up to the year 2022. A fictatious persona is first generated where this person is, by design, between 18 and 75 in 2022. The persona is stored as persona.json in the directory "mydir".
  
See our LICENSE file for licensing details.
  
