using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Graph : MonoBehaviour 
{
	public GameObject vertex; // vertex prefab to copy when instantiating
	public GameObject edge; // edge prefab...
	private List<Vertex> V = new List<Vertex>(); // List of Vertex MonoBehaviors


	void Start ()
	{

	}


	void Update ()
	{
		if (Input.GetKeyDown ("v"))
		{
			CreateVertex ();
		}
	}


	Vertex CreateVertex (Vector3 position = default(Vector3))
	{
		// instantiate Vertex prefab, set parent to this.transform, get corresponding monobehavior
		Vertex vertexMono = Instantiate (vertex, this.transform).GetComponent<Vertex> ();

		// add monobehavior to vertex list
		V.Add (vertexMono);

		// master relation
		vertexMono.SetMaster (this);

		// set position
		vertexMono.transform.localPosition = position;

		return vertexMono;
	}


	Edge CreateEdge ()
	{
		// instantiate Edge prefab, set parent to this.transform, get corresponding monobehavior
		Edge edgeMono = Instantiate (edge, this.transform).GetComponent<Edge> ();

		// master relation
		edgeMono.SetMaster (this);

		return edgeMono;
	}


	Edge ConnectVertices(Vertex startVertex, Vertex endVertex, float weight=1f, bool directed=false)
	{
		// create an edge
		Edge edgeMono = CreateEdge ();

		// set edge weight
		edgeMono.SetWeight (weight);

		// set directed
		edgeMono.SetDirected (directed);

		// set endpoints
		edgeMono.SetStartVertex (startVertex);
		edgeMono.SetEndVertex (endVertex);

		return edgeMono;
	}
}
