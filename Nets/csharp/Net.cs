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

    // TODO
    public NeuralNet(string file_path)
    {
        propagation_key = 0;
    }

    public void run(float[] inputs, float[] desired_outputs)
    {
        float[] predicted = prop_forward(inputs);
        prop_backward(desired_outputs);
        correct_weights();
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