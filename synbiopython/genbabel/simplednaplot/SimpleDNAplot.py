# pylint: disable=E0401,C0103,R0912,R0914,R0915,R1702
"""
Synbiopython (c) Global BioFoundry Alliance 2020

Synbiopython is licensed under the MIT License.

This module is to implement the simple plotting of the gene circuit using the modified code
from quickplot.py in DNAplotlib library
# added quickplot style for writing Regulations.
# added new Regulation type: Derepression

Reference:
    https://github.com/VoigtLab/dnaplotlib

Install:
    pip install dnaplotlib
"""

import re
import matplotlib
import matplotlib.pyplot as plt
import dnaplotlib as dpl


class SimpleDNAplot:
    """Class to generate SBOL visual compliant gene circuit diagram.
    Regulation type: Connection, Activation, Repression, Derepression
    Each of the part will be numbered sequentially based on the part type/module
    from left to right starting from index 0.
    Example: p0-r0-c0-t0-p1-r1-c1-t1 for two modules with promoter, RBS, coding
    region, and terminator.
    Input = "p.pTet r.rbs34 c.orange.LacI t p.pLac r.rbs32 c.green.TetR t"
    Regulations = "c0->p1.Repression c1->p0.Repression"
    # The default color is black if color is not specified
    """

    def set_circuit_design(self, Input, Regulation=None):
        """Generate the dictionary list containing circuit design information.

        :param Input: a string containing the individual type of part, followed by color
            and name separated by a space.
        :type Input: str
        :param Regulation: a string containing the from_part to the to_part connected
            by an arrow. Type of interaction is specified after the topart followed
            by the color. Default color of black is used is not specified.
        :type Regulation: str, optional
        :return: The part information and Regulations stored in the form of list of dictionaries.
        :rtype: list of dict
        """

        # Types mapping
        types = {}
        types["p"] = "Promoter"
        types["i"] = "Ribozyme"
        types["r"] = "RBS"
        types["c"] = "CDS"
        types["t"] = "Terminator"
        types["s"] = "Spacer"
        types["="] = "Scar"
        types["o"] = "Origin"
        types["es"] = "EmptySpace"

        # Colours mapping
        colors = {}
        colors["black"] = (0.00, 0.00, 0.00)
        colors["gray"] = (0.60, 0.60, 0.60)
        colors["red"] = (0.89, 0.10, 0.11)
        colors["orange"] = (1.00, 0.50, 0.00)
        colors["yellow"] = (1.00, 1.00, 0.00)
        colors["white"] = (1.00, 1.00, 1.00)
        colors["green"] = (0.20, 0.63, 0.17)
        colors["blue"] = (0.12, 0.47, 0.71)
        colors["purple"] = (0.42, 0.24, 0.60)
        colors["lightred"] = (0.98, 0.60, 0.60)
        colors["lightorange"] = (0.99, 0.75, 0.44)
        colors["lightyellow"] = (1.00, 1.00, 0.60)
        colors["lightgreen"] = (0.70, 0.87, 0.54)
        colors["lightblue"] = (0.65, 0.81, 0.89)
        colors["lightpurple"] = (0.79, 0.70, 0.84)

        # Generate the parts list from the arguments
        part_list = []
        part_length = []
        part_idx = 1
        for el in Input.split(" "):
            if el != "":
                part_parts = el.split(".")
                part_label = ""
                part_rgb = (0, 0, 0)
                if len(part_parts) >= 1:
                    part_short_type = part_parts[0]
                    part_fwd = True
                    if part_short_type[0] == "-":
                        part_fwd = False
                        part_short_type = el[1]
                    if part_short_type in types.keys():
                        part_type = types[part_short_type]

                    else:
                        print("Error! Please specify the correct part type!")

                    part_label_yoffset = -5
                    part_label_color = "black"
                    part_label_size = 9
                    part_label_style = "normal"
                    if part_parts[0][0] == "-":
                        part_label_yoffset = 5

                    if len(part_parts) >= 2:
                        part_color = part_parts[1]
                        if part_color in colors.keys():
                            part_rgb = colors[part_color]
                        else:
                            part_label = part_parts[1]

                        if len(part_parts) >= 3:
                            part_label = part_parts[2]
                        elif part_label == "":
                            part_label = ""

                        if part_short_type == "c":
                            part_label_yoffset = 0
                            part_label_color = "white"
                            part_label_size = 10
                            part_label_style = "italic"
                        elif part_short_type == "o":
                            part_label_yoffset = -10
                            part_label_color = "black"
                            part_label_size = 8
                            part_label_style = "normal"
                        elif part_short_type in ("p", "r"):
                            part_label_yoffset = -5
                            part_label_color = "black"
                            part_label_size = 8
                            part_label_style = "normal"
                        else:
                            part_label_yoffset = -5
                            part_label_color = "black"
                            part_label_size = 8
                            part_label_style = "normal"
                            if part_parts[0][0] == "-":
                                part_label_yoffset = 5

                    part_list.append(
                        {
                            "name": str(part_idx),
                            "type": part_type,
                            "fwd": part_fwd,
                            "opts": {
                                "color": part_rgb,
                                "label": part_label,
                                "label_y_offset": part_label_yoffset,
                                "label_color": part_label_color,
                                "label_size": part_label_size,
                                "label_style": part_label_style,
                            },
                        }
                    )
                    part_length.append(part_short_type)

            part_idx = part_idx + 1

        # update the part_length to include the numbering to be used for regulations
        for i in types:
            n = 0
            for a, _ in enumerate(part_length):
                if part_length[a] is i:
                    part_length[a] = i + str(n)
                    n += 1

        print("part_length", part_length)

        # Update the Regulations from the arguments
        Regulations = []

        if Regulation is not None:
            Reg_list = Regulation.split(" ")

            for r, _ in enumerate(Reg_list):
                first_yoffset = 0
                second_yoffset = 0
                arc_height_const = 17
                arc_height_spacing = 4
                arc_height_start = 13

                if Reg_list[r] != "":
                    reg_parts = Reg_list[r].split(".")
                    if "Derepression" in reg_parts[1]:
                        first_yoffset = -5
                        second_yoffset = 4.5
                        reg_type = "Repression"
                    elif "Activation2" in reg_parts[1]:
                        first_yoffset = -5
                        second_yoffset = 4.5
                        reg_type = "Activation"
                    else:
                        second_yoffset = 0
                        reg_type = reg_parts[1]
                    tofr_part = reg_parts[0].split("->")
                    fr_part = tofr_part[0]
                    to_part = tofr_part[1]
                    fr_part_len = self.compute_dnalength(fr_part, part_length)
                    to_part_len = self.compute_dnalength(to_part, part_length)

                    fwd = (fr_part_len <= to_part_len) or (
                        "Derepression" in reg_parts[1]
                    )

                    if len(reg_parts) > 2:
                        reg_color = reg_parts[2]

                        if reg_color in colors.keys():
                            reg_rgb = colors[reg_color]
                    else:
                        reg_rgb = colors["black"]

                    arc_height_spacing = arc_height_spacing + first_yoffset
                    arc_height_const = arc_height_const + second_yoffset
                    arc_height_start = arc_height_start + second_yoffset
                    arc_height_end = arc_height_start * 1
                    arc_height = arc_height_const + arc_height_spacing

                    Regulations.append(
                        {
                            "type": reg_type,
                            "from_part": {"start": fr_part_len, "end": fr_part_len},
                            "to_part": {
                                "start": to_part_len,
                                "end": to_part_len,
                                "fwd": fwd,
                            },
                            "opts": {
                                "color": reg_rgb,
                                "linewidth": 1.5,
                                "arc_height_const": arc_height_const,
                                "arc_height_spacing": arc_height_spacing,
                                "arc_height_start": arc_height_start,
                                "arc_height_end": arc_height_end,
                                "arc_height": arc_height,
                                "arrowhead_length": 2,
                            },
                        }
                    )

            # Modify the plot of the last Repression before Derepression
            indices = [i for i, s in enumerate(Reg_list) if "Derepression" in s]
            indices2 = [i for i, s in enumerate(Reg_list) if "Activation2" in s]

            Rep = []
            for i, _ in enumerate(indices):
                ind = []
                for j in range(indices[i]):
                    if "Repression" in Reg_list[j]:
                        ind.append(j)
                Rep.append({str(indices[i]): ind})

            Act = []
            for i, _ in enumerate(indices2):
                ind = []
                for j in range(indices2[i]):
                    if "Activation" in Reg_list[j]:
                        ind.append(j)
                Act.append({str(indices2[i]): ind})

            arc_height_const = 17
            arc_height_spacing = 4
            first_yoffset = -5
            if len(Rep) != 0:
                for i in Rep:
                    arc_height_spacing = arc_height_spacing + first_yoffset
                    arc_height = arc_height_const + arc_height_spacing
                    Regulations[list(i.values())[0][-1]]["opts"][
                        "arc_height_spacing"
                    ] = arc_height_spacing
                    Regulations[list(i.values())[0][-1]]["opts"][
                        "arc_height"
                    ] = arc_height

            arc_height_const = 17
            arc_height_spacing = 4
            first_yoffset = -5
            if len(Act) != 0:
                for i in Act:
                    arc_height_spacing = arc_height_spacing + first_yoffset
                    arc_height = arc_height_const + arc_height_spacing
                    Regulations[list(i.values())[0][-1]]["opts"][
                        "arc_height_spacing"
                    ] = arc_height_spacing
                    Regulations[list(i.values())[0][-1]]["opts"][
                        "arc_height"
                    ] = arc_height

        else:
            Regulations = None

        return part_list, Regulations

    @staticmethod
    def compute_dnalength(part, part_length):
        """Calculate the position for the to_part or from_part for plotting arrows
        automatically.

        :param part: the to_part or from_part
        :type part: str
        :param part_length: all the parts with sequential numbering starting from 0
        :type part_length: list of str
        :return: dna length
        :rtype: float
        """

        # dna length
        dnalen = {}
        dnalen["p"] = 14.0
        dnalen["i"] = 9.0
        dnalen["r"] = 14.0
        dnalen["c"] = 32.0
        dnalen["t"] = 12.0
        dnalen["s"] = 10.0
        dnalen["="] = 7.0
        dnalen["o"] = 17.0
        dnalen["es"] = 20.0

        dnalength = 0
        ind = part_length.index(part)

        for i in range(ind + 1):
            p = re.sub(r"\d", "", part_length[i])
            if p in dnalen.keys():
                if i is ind:
                    dnalength += 0.5 * dnalen[p]

                else:
                    dnalength += dnalen[p]

        return dnalength

    def plot_circuit(self, Input, Regulation=None, savefig=None):
        """Plot the SBOL-compliant gene circuit figure.

        :param Input: Input design from users
        :type Input: str
        :param Regulation: Regulation strings from users
        :type Regulation: str
        :param savefig: path to store the output figure
        :type savefig: str, optional
        :return: max dna design length and export the gene circuit figure
        :rtype: float
        """

        # matplotlib.use("Qt5Agg")
        matplotlib.use("Agg")

        dr = dpl.DNARenderer(linewidth=1.5)

        # Process the arguments
        design, Regulations = self.set_circuit_design(Input, Regulation)

        reg_renderers = dr.std_reg_renderers()
        part_renderers = dr.SBOL_part_renderers()

        # Generate the figure
        fig = plt.figure(figsize=(1.0, 1.0), dpi=100)
        ax = fig.add_subplot(1, 1, 1)

        # Plot the design
        dna_start, dna_end = dr.renderDNA(
            ax, design, part_renderers, Regulations, reg_renderers
        )
        max_dna_len = dna_end - dna_start

        # print("Max Dna length: ", max_dna_len)

        # Format the axis
        ax.set_xticks([])
        ax.set_yticks([])

        # Set bounds
        ax.set_xlim([(-0.0 * max_dna_len), max_dna_len + (0.0 * max_dna_len)])
        ax.set_ylim([-25, 25])
        ax.set_aspect("equal")
        ax.set_axis_off()

        # Update the size of the figure to fit the constructs drawn
        fig_x_dim = max_dna_len / 30
        # print("x_dim: ", fig_x_dim)
        if fig_x_dim < 1.0:
            fig_x_dim = 1.0
        fig_y_dim = 1.8
        plt.gcf().set_size_inches(fig_x_dim, fig_y_dim, forward=True)

        # Save the figure
        plt.tight_layout()

        if savefig is not None:
            fig.savefig(savefig, transparent=True, dpi=300)
        # plt.show()

        return max_dna_len, fig
