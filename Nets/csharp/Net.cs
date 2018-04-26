using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NeuralNet
{
    public List<Layer> layers = new List<Layer>();
    public Layer input_layer;
    public Layer output_layer;

    public float learning_rate = 0.01f;

    private int propagation_key;

    public NeuralNet(string file_path)
    {
        List<String[]> adjacencies = new List<String[]>();
        string[] lines = System.IO.File.ReadAllLines(file_path);
        int i = 0;
        while (i < lines.Length)
        {
            string[] line = lines[i].Split(';');
            string activation = line[1];
            int node_count = Int32.Parse(line[3]);
            float bias = float.Parse(line[4]);
            float leakiness = float.Parse(line[5]);
            float bound = float.Parse(line[6]);
            adjacencies.Add(line[7].Split(','));
            Layer new_layer = new Layer(this, activation, node_count, leakiness, bound, bias);
            Debug.Log(string.Format("Creating new layer {0} with activation {1}, node_count {2}, leakiness {3}, bound {4}, and bias{5}", i, activation, node_count, leakiness, bound, bias));
            layers.Add(new_layer);
            i++;
        }
        input_layer = layers[0];
        output_layer = layers[i - 1];

        i = 0;
        while (i < layers.Count)
        {
            int j = 0;
            while (j < layers.Count)
            {
                if (adjacencies[i][j] != "None")
                {
                    string[] weight_details = adjacencies[i][j].Split('|');
                    float weight = float.Parse(weight_details[0]);
                    float noise = float.Parse(weight_details[1]);
                    layers[i].add_output_layer(layers[j], weight, noise);
                    Debug.Log(string.Format("Connecting Layer {0} to layer {1} with weight {2} and noise{3}", i, j, weight, noise));
                }
                j++;
            }
            i++;
        }
    }

    public float[] run(float[] inputs, float[] desired_outputs)
    {
        float[] predicted = prop_forward(inputs);
        prop_backward(desired_outputs);
        correct_weights();
        correct_bias();
        return predicted;
    }

    public float[] prop_forward(float[] inputs)
    {
        reset_layer_inputs();

        input_layer.set_inputs(inputs);
        input_layer.prop_forward(propagation_key);
        iterate_key();

        return output_layer.outputs;
    }

    public void prop_backward(float[] desired_outputs)
    {
        reset_layer_deltas();

        output_layer.set_deltas_by_comparison(desired_outputs);
        output_layer.prop_backward(propagation_key);
        iterate_key();
    }

    public void correct_weights()
    {
        int i = 0;
        while (i < layers.Count)
        {
            layers[i].correct_weights_ahead();
            i++;
        }
    }

    public void correct_bias()
    {
        int i = 0;
        while (i < layers.Count)
        {
            layers[i].correct_bias();
            i++;
        }
    }

    public void reset_layer_inputs()
    {
        int i = 0;
        while (i < layers.Count)
        {
            layers[i].reset_inputs();
            i++;
        }
    }

    public void reset_layer_deltas()
    {
        int i = 0;
        while (i < layers.Count)
        {
            layers[i].reset_deltas();
            i++;
        }
    }

    private void iterate_key()
    {
        propagation_key = (propagation_key + 1) % 100;
    }
}