FROM python
RUN pip install networkx numpy ortools git+https://github.com/snkas/python-ortools-lp-parser.git@v1.5.2
COPY code /project4/code
COPY ground_truth /project4/ground_truth
COPY myself/output/a /project4/myself/output/a
COPY myself/output/b /project4/myself/output/b
RUN mkdir /project4/myself/output/c

WORKDIR /project4/code

CMD python skeleton_c.py && python evaluator_myself.py