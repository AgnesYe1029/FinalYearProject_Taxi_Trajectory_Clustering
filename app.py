from flask import Flask, render_template, render_template_string
from trajectory_clustering import TrajectoryClustering
import folium

app =  Flask(__name__)
tc = TrajectoryClustering()

@app.route('/')
def index():
    trajs, traj_xy = tc.all_trajectories()
    m = tc.plot_all_trajectories_using_folium(traj_to_plot=trajs)

    # set the iframe width and height
    m.get_root().width = "800px"
    m.get_root().height = "600px"
    iframe = m.get_root()._repr_html_()
    traj_groups = tc.grouped_trajectories()
    grouped_iframes = []
    for grp in traj_groups:
        label_group_start = list(grp[0][0])
        m = folium.Map(location=label_group_start, zoom_start=10)
        for index, x in enumerate(grp):
            folium.PolyLine(grp[index]).add_to(m)
        m.get_root().width = "400px"
        m.get_root().height = "300px"
        grouped_iframes.append(m.get_root()._repr_html_())

    return render_template('index.html', iframe=iframe, grouped_traj = grouped_iframes)



if __name__ ==  "__main__":
    app.run(debug=True)