import React from 'react'
import Graph from './Components/Graph'
import Graph2 from './Components/Graph2'

export default function App() {
	const [data, setData] = React.useState();
	const [loading, setLoading] = React.useState(true);
	const rawData = async () => {
		try {
			const response = await fetch('http://localhost:5000/*');
			const jsonData = await response.json();
			setData(jsonData);
			setLoading(false);
		} catch (err) {
			console.error(err.message);
		}
	}

	React.useEffect(() => {
		rawData();
	}, []);

	return (
		<div className="App">
			<header className="App-header"><h1>BaseBool Dashboard</h1></header>
			<Graph2
				data = {data}
				loading = {loading}
			/>
			<Graph
				data = {data}
			/>
		</div>
	);
}
