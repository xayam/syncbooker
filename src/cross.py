import heapq
import re
import bokeh
import bokeh.models
import bokeh.plotting
import cv2
import numpy as np
import os
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow_text import SentencepieceTokenizer
import sklearn.metrics.pairwise
from PIL import Image
from matplotlib import cm
import matplotlib.pyplot as plt

# from simpleneighbors import SimpleNeighbors
from tqdm import tqdm
from tqdm import trange


def visualize_similarity(embeddings_1, embeddings_2, labels_1, labels_2,
                         plot_title,
                         plot_width=1200, plot_height=600,
                         xaxis_font_size='12pt', yaxis_font_size='12pt'):
    assert len(embeddings_1) == len(labels_1)
    assert len(embeddings_2) == len(labels_2)

    # arccos based text similarity (Yang et al. 2019; Cer et al. 2019)
    sim = 1 - np.arccos(
        sklearn.metrics.pairwise.cosine_similarity(embeddings_1,
                                                   embeddings_2)) / np.pi

    embeddings_1_col, embeddings_2_col, sim_col = [], [], []
    for i in range(len(embeddings_1)):
        for j in range(len(embeddings_2)):
            embeddings_1_col.append(labels_1[i])
            embeddings_2_col.append(labels_2[j])
            sim_col.append(sim[i][j])
    df = pd.DataFrame(zip(embeddings_1_col, embeddings_2_col, sim_col),
                      columns=['embeddings_1', 'embeddings_2', 'sim'])

    mapper = bokeh.models.LinearColorMapper(
        palette=[*reversed(bokeh.palettes.YlOrRd[9])], low=df.sim.min(),
        high=df.sim.max())

    p = bokeh.plotting.figure(title=plot_title, x_range=labels_1,
                              x_axis_location="above",
                              y_range=[*reversed(labels_2)],
                              plot_width=plot_width, plot_height=plot_height,
                              tools="save", toolbar_location='below', tooltips=[
            ('pair', '@embeddings_1 ||| @embeddings_2'),
            ('sim', '@sim')])
    p.rect(x="embeddings_1", y="embeddings_2", width=1, height=1, source=df,
           fill_color={'field': 'sim', 'transform': mapper}, line_color=None)

    p.title.text_font_size = '12pt'
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_standoff = 16
    p.xaxis.major_label_text_font_size = xaxis_font_size
    p.xaxis.major_label_orientation = 0.25 * np.pi
    p.yaxis.major_label_text_font_size = yaxis_font_size
    p.min_border_right = 300

    bokeh.io.export_png(bokeh.io.curdoc(), filename="cross.png")
    bokeh.io.show(p)


module_url = 'https://tfhub.dev/google/universal-sentence-encoder-multilingual/3'

model = hub.load(module_url)


def embed_text(input):
    return model(input)


def get_sim(html, map):
    labels_1 = re.findall(r"<p>(.*?)</p>", html, flags=re.DOTALL | re.UNICODE)
    labels_2 = map
    sim = [[0 for _ in range(len(labels_2))] for _ in range(len(labels_1))]
    for i in range(len(labels_1)):
        for j in range(len(labels_2)):
            if labels_1[i].find(labels_2[j]) > -1:
                sim[i][j] = 100
    L_start = []
    L_end = []
    length = 0
    for i in labels_1:
        L_start.append(length)
        length += len(i)
        L_end.append(length)

    sim = np.asarray(sim)

    return sim, labels_1, L_start, L_end


def get_sim_v2(book):
    with open(f"data/{book}/orig.html", mode="r", encoding="UTF-8") as f:
        orig_html = f.read()
    with open(f"data/{book}/orig2.html", mode="r", encoding="UTF-8") as f:
        orig_html2 = f.read()

    labels_1 = re.findall(r"<p>(.*?)</p>", orig_html, flags=re.DOTALL | re.UNICODE)
    labels_2 = re.findall(r"<p>(.*?)</p>", orig_html2, flags=re.DOTALL | re.UNICODE)
    embeddings_1 = embed_text(labels_1)
    embeddings_2 = embed_text(labels_2)

    sim = 1 - np.arccos(
        sklearn.metrics.pairwise.cosine_similarity(embeddings_1,
                                                   embeddings_2)) / np.pi
    for i in range(len(sim)):
        for j in range(len(sim[i])):
            if sim[i][j] < 0.63:
                sim[i][j] = 0
            else:
                sim[i][j] = 100
    L_end = []
    length = 0
    for i in labels_1:
        length += len(i)
        L_end.append(length)
    R_end = []
    length = 0
    for i in labels_2:
        length += len(i)
        R_end.append(length)

    return sim, labels_1, labels_2, L_end, R_end


def find_shortest_paths(graph, start_point):
    # initialize graphs to track if a point is visited,
    # current calculated distance from start to point,
    # and previous point taken to get to current point
    visited = [[True if graph[row][col] is None else False
                for col in range(len(graph[row]))] for row in range(len(graph))]
    distance = [[float('inf') for col in row] for row in graph]
    distance[start_point[0]][start_point[1]] = 0
    prev_point = [[None for col in row] for row in graph]
    n, m = len(graph), len(graph[0])
    visited_count = 0
    for row in range(len(visited)):
        for col in range(len(visited[row])):
            if visited[row][col]:
                visited_count += 1
    number_of_points = n * m
    directions = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9),
                  (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0),
                  (1, 1)  # , (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)
                  ]
    min_heap = []

    # min_heap item format:
    # (pt's dist from start on this path, pt's row, pt's col)
    heapq.heappush(min_heap, (distance[start_point[0]][start_point[1]], start_point[0], start_point[1]))

    while visited_count < number_of_points:
        current_point = heapq.heappop(min_heap)
        distance_from_start, row, col = current_point
        for direction in directions:
            new_row, new_col = row + direction[0], col + direction[1]
            if -1 < new_row < n and -1 < new_col < m and not visited[new_row][new_col]:
                dist_to_new_point = distance_from_start + graph[new_row][new_col]
                if dist_to_new_point < distance[new_row][new_col]:
                    distance[new_row][new_col] = dist_to_new_point
                    prev_point[new_row][new_col] = (row, col)
                    heapq.heappush(min_heap, (dist_to_new_point, new_row, new_col))
        visited[row][col] = True
        visited_count += 1

    return distance, prev_point


def find_shortest_path(prev_point_graph, end_point):
    shortest_path = []
    current_point = end_point
    while current_point is not None:
        shortest_path.append(current_point)
        current_point = prev_point_graph[current_point[0]][current_point[1]]
    shortest_path.reverse()
    return shortest_path


if __name__ == "__main__":
    graph = [
        [1, 1, 6, 3, 7, 5, 1, 7, 4, 200],
        [1, 3, 8, 1, 3, 7, 3, 6, 7, 2],
        [2, 1, 3, 6, 5, None, 1, 3, 2, 8],
        [3, 6, 9, 4, 9, 3, 1, 5, 6, 9],
        [7, 4, 6, 3, 4, 1, 7, 1, 1, 1],
        [1, 3, 1, 9, 1, 2, 8, 1, 3, 7],
        [1, 3, 5, 9, 9, 1, 2, 4, 2, 1],
        [3, 1, 2, 5, 4, 2, 1, 6, 3, 9],
        [1, 2, 9, 3, 1, 3, 8, 5, 2, 1],
        [2, 3, 1, 1, 9, 4, 4, 5, 8, 1],
    ]
    distance, prev_point = find_shortest_paths(graph, (0, 0))
    print(find_shortest_path(prev_point, (9, 9)))
