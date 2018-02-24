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

	// params for selection and display
	public bool isSelected = false;
	private MeshRenderer renderer;
	public Material unselectedMaterial;
	public Material selectedMaterial;

	// size (use as weight for centroid calculation)
	private int size = 1;

	// vertex communication params
	public bool isReceiving = false;


	void Start ()
	{
		renderer = GetComponent<MeshRenderer> ();
	}


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


	public void SetSelected(bool isSelected)
	{
		if (this.isSelected == !isSelected)
		{
			this.isSelected = isSelected;
			if (isSelected)
			{
				renderer.material = selectedMaterial;
			}
			else
			{
				renderer.material = unselectedMaterial;
			}
		}
	}


	public void ToggleSelected ()
	{
		SetSelected (!isSelected);
	}


	public int GetSize ()
	{
		return size;
	}


	public void SetSize (int size)
	{
		this.size = size;
	}

	
	public void SelectPing ()
	{
		int index = 0;
		while (index < adjEdge.Count)
		{
			adjEdge [index].PingSelect (this);
			index++;
		}
	}
}
