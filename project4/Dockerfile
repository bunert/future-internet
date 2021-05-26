FROM python
RUN pip install networkx numpy ortools git+https://github.com/snkas/python-ortools-lp-parser.git@v1.5.2
COPY code project4/code
COPY ground_truth project4/ground_truth
RUN mkdir -p /project4/myself/output/a
RUN mkdir -p /project4/myself/output/b
RUN mkdir -p /project4/myself/output/c
WORKDIR /project4/code

#CMD python skeleton_a.py && python skeleton_b.py && python skeleton_c.py && python evaluator_myself.py
CMD python skeleton_c.py && python evaluator_myself.py