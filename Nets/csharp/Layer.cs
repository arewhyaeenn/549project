using UnityEngine;
using System;
using System.Collections;
using System.Collections.Generic;

public class Layer
{
    public NeuralNet master;
    public int node_count;

    public float[] inputs;
    public float[] biases;
    public float[] outputs;
    public float[] differentials;
    public float[] deltas;

    private float initial_weight;
    private float weight_noise;
    public List<float[,]> weights = new List<float[,]>();

    public List<Layer> incoming_layers = new List<Layer>();
    public List<Layer> outgoing_layers = new List<Layer>();
    public List<int> incoming_to_self = new List<int>();

    public delegate void Activation();
    public Activation activate;

    private float bound; // bound for relu, log and exp activators
    private float leakiness; // leakiness for sigmoid, relu, log, and exp activators = minimum differential
    private float ln_bound; // to avoid having to recalculate log(bound) for log and exp activators

    public int propagation_key = -1;

    public Layer(NeuralNet master, string activation, int node_count, float leakiness = 0f, float bound = 10f, float initial_bias = 0f, float initial_weight = 0f, float weight_noise = 0.1f)
    {
        this.master = master;

        this.node_count = node_count;
        inputs = new float[node_count];
        outputs = new float[node_count];
        differentials = new float[node_count];
        deltas = new float[node_count];

        this.initial_weight = initial_weight;
        this.weight_noise = weight_noise;

        biases = new float[node_count];
        if (initial_bias != 0f)
        {
            int i = 0;
            while (i < node_count)
            {
                biases[i] = initial_bias;
                i++;
            }
        }

        switch (activation)
        {
            case ("Sigmoid"):
                activate = sigmoid_activate;
                this.leakiness = leakiness;
                break;
            case ("ReLU"):
                activate = relu_activate;
                this.bound = bound;
                this.leakiness = leakiness;
                break;
            case ("Logarithmic"):
                activate = log_activate;
                this.bound = bound;
                this.ln_bound = Mathf.Log(bound);
                this.leakiness = leakiness;
                break;
            case ("Exponential"):
                activate = exp_activate;
                this.bound = bound;
                this.ln_bound = Mathf.Log(bound);
                this.leakiness = leakiness;
                break;
            case ("Identity"):
                activate = identity_activate;
                int i = 0;
                while (i < node_count)
                {
                    differentials[i] = 1;
                    i++;
                }
                break;
            default:
                throw new System.ArgumentException(string.Format("Invalid Activation: {0}", activation));
        }
    }

    public void prop_forward(int key)
    {
        if (propagation_key != key)
        {
            int i = 0;
            while (i < incoming_layers.Count)
            {
                incoming_layers[i].prop_forward(key);
                i++;
            }

            propagation_key = key;

            i = 0;
            while (i < node_count)
            {
                inputs[i] += biases[i];
                i++;
            }
            activate();

            i = 0;
            while (i < outgoing_layers.Count)
            {
                Layer layer = outgoing_layers[i];
                int j = 0;
                while (j < node_count)
                {
                    float value = outputs[j];
                    int k = 0;
                    while (k < layer.node_count)
                    {
                        layer.add_value_at_index(value * weights[i][j, k], k);
                        k++;
                    }
                    j++;
                }
                layer.prop_forward(key);
                i++;
            }
        }
    }

    public void prop_backward(int key)
    {
        if (propagation_key != key)
        {
            int i = 0;
            while (i < outgoing_layers.Count)
            {
                outgoing_layers[i].prop_backward(key);
                i++;
            }

            key = propagation_key;

            i = 0;
            while (i < node_count)
            {
                deltas[i] *= differentials[i];
                i++;
            }

            i = 0;
            while (i < incoming_layers.Count)
            {
                Layer layer = incoming_layers[i];
                int inverse_index = incoming_to_self[i];
                int j = 0;
                while (j < layer.node_count)
                {
                    int k = 0;
                    while (k < node_count)
                    {
                        layer.add_delta_at_index(deltas[k] * layer.weights[inverse_index][j, k], j);
                        k++;
                    }
                    j++;
                }
                i++;
                layer.prop_backward(key);
            }
        }
    }

    public void correct_weights_ahead()
    {
        int i = 0;
        while (i < outgoing_layers.Count)
        {
            Layer layer = outgoing_layers[i];
            int j = 0;
            while (j < layer.node_count)
            {
                float delta = layer.deltas[j];
                int k = 0;
                while (k < node_count)
                {
                    weights[i][k, j] += master.learning_rate * outputs[k] * delta;
                    k++;
                }
                j++;
            }
            i++;
        }
    }

    public void correct_bias()
    {
        int i = 0;
        while (i < node_count)
        {
            biases[i] += master.learning_rate * deltas[i];
            i++;
        }
    }

    public void set_inputs(float[] inputs)
    {
        if (inputs.Length == node_count)
        {
            this.inputs = inputs;
        }
        else
        {
            throw new System.ArgumentException("Layer received invalid number of inputs.");
        }
    }

    public void set_deltas_by_comparison(float[] desired_outputs)
    {
        if (desired_outputs.Length == node_count)
        {
            int i = 0;
            while (i < node_count)
            {
                deltas[i] = (desired_outputs[i] - outputs[i]) * differentials[i];
                i++;
            }
        }
        else
        {
            throw new System.ArgumentException("Layer received invalid number of desired outputs.");
        }
    }

    public void inherit_deltas(Layer layer)
    {
        this.deltas = layer.deltas;
    }

    public void add_value_at_index(float value, int index)
    {
        inputs[index] += value;
    }

    public void add_delta_at_index(float value, int index)
    {
        deltas[index] += value;
    }

    public void reset_inputs()
    {
        inputs = new float[node_count];
    }

    public void reset_deltas()
    {
        deltas = new float[node_count];
    }

    public void add_output_layer(Layer layer)
    {
        layer.add_input_layer(this, outgoing_layers.Count);
        outgoing_layers.Add(layer);
        float[,] new_weights = new float[node_count, layer.node_count];
        if (initial_weight != 0f)
        {
            int i = 0;
            while (i < node_count)
            {
                int j = 0;
                while (j < layer.node_count)
                {
                    new_weights[i, j] = initial_weight;
                    j++;
                }
                i++;
            }
        }
        if (weight_noise != 0f)
        {
            int i = 0;
            while (i < node_count)
            {
                int j = 0;
                while (j < layer.node_count)
                {
                    new_weights[i, j] += UnityEngine.Random.Range(-weight_noise, weight_noise);
                    j++;
                }
                i++;
            }
        }
        weights.Add(new_weights);
    }

    public void add_output_layer(Layer layer, float mean_weight, float noise)
    {
        layer.add_input_layer(this, outgoing_layers.Count);
        outgoing_layers.Add(layer);
        float[,] new_weights = new float[node_count, layer.node_count];
        if (mean_weight != 0f)
        {
            int i = 0;
            while (i < node_count)
            {
                int j = 0;
                while (j < layer.node_count)
                {
                    new_weights[i, j] = mean_weight;
                    j++;
                }
                i++;
            }
        }
        if (noise != 0f)
        {
            int i = 0;
            while (i < node_count)
            {
                int j = 0;
                while (j < layer.node_count)
                {
                    new_weights[i, j] += UnityEngine.Random.Range(-noise, noise);
                    j++;
                }
                i++;
            }
        }
        weights.Add(new_weights);
    }

    public void add_input_layer(Layer layer, int index)
    {
        this.incoming_layers.Add(layer);
        incoming_to_self.Add(index);
    }

    public void sigmoid_activate()
    {
        int i = 0;
        while (i < node_count)
        {
            outputs[i] = 1 / (1 + Mathf.Exp(-inputs[i]));
            differentials[i] = Mathf.Max(outputs[i] * (1 - outputs[i]), leakiness);
            i++;
        }
    }

    public void relu_activate()
    {
        int i = 0;
        while (i < node_count)
        {
            float input = inputs[i];
            if (input > bound)
            {
                outputs[i] = bound;
                differentials[i] = leakiness;
            }
            else if (input > 0)
            {
                outputs[i] = input;
                differentials[i] = 1;
            }
            else
            {
                outputs[i] = 0;
                differentials[i] = leakiness;
            }
            i++;
        }
    }

    public void log_activate()
    {
        int i = 0;
        while (i < node_count)
        {
            float input = inputs[i];
            if (input > bound)
            {
                outputs[i] = ln_bound + 2 - Mathf.Exp(-input / bound + 1);
                differentials[i] = Mathf.Max((ln_bound + 2 - outputs[i]) / bound, leakiness);
            }
            else if (input > 1)
            {
                outputs[i] = Mathf.Log(input);
                differentials[i] = 1 / input;
            }
            else
            {
                outputs[i] = Mathf.Exp(input - 1);
                differentials[i] = Mathf.Max(outputs[i], leakiness);
            }
            i++;
        }
    }

    public void exp_activate()
    {
        int i = 0;
        while (i < node_count)
        {
            float input = inputs[i];
            if (input > ln_bound)
            {
                outputs[i] = 2 - Mathf.Exp(ln_bound - input);
                differentials[i] = Mathf.Max(2 - outputs[i], leakiness);
            }
            else
            {
                outputs[i] = Mathf.Exp(input) / bound;
                differentials[i] = Mathf.Max(outputs[i], leakiness);
            }
            i++;
        }
    }

    public void identity_activate()
    {
        int i = 0;
        while (i < node_count)
        {
            outputs[i] = inputs[i];
            i++;
        }
    }
}