using System.Collections;
using System.Collections.Generic;
using UnityEngine;


public class Vertex : MonoBehaviour
{
	// Graph
	private Graph master;

	// Adjacencies
	private List<Edge> adjEdge = new List<Edge>();
	//TODO: keep adjacencies sorted by weight
	//	use binary search to add / remove
	//	this will increase AddConnection complexity to O(log(n)) from O(1)
	//	but it will lower RemoveConnection complexity from O(n) to O(log(n))


	void Update ()
	{
		
	}


	public void SetMaster (Graph master)
	{
		this.master = master;
	}
		

	public void AddConnection (Edge edge)
	{
		adjEdge.Add (edge);
	}


	public void RemoveConnection(Edge edge)
	{
		adjEdge.Remove (edge);
	}


	public void LogAdjacency()
	{
		Debug.Log (this.adjEdge.Count);
	}
}
