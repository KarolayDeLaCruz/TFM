#pragma once
#include <WinSock2.h>
#include "catClass.h"
#include "communications.h"
#include "functions.h"
#include <fstream>
#include <sstream>
#include <iostream>
#include <vector>
#include <algorithm>
#include <stdlib.h>     
#include <time.h>       
using namespace std;

SOCKET ClientSocket;
int main(){
	srand(time(NULL));
	if (startCommunication() == 0) { return 1; }  // si el sistema no conecta, finalizar
	/*	cout << "explore" << endl;
	sendMessage({ 2, 2, 10 });
	sendMessage({ 2, 2, 10 });
	sendMessage({ 2, 2, 10 });
	sendMessage({ 2, 3, 10 });
	sendMessage({ 2, 4, 10 });
	sendMessage({ 2, 5, 10 });
	sendMessage({ 2, 6, 10 });
	sendMessage({ 2, 4, 10 });
	sendMessage({ 2, 7, 10 });
	sendMessage({ 2, 18, 10 });
	getchar();
	*/
	/*
	cout << "groom" << endl;
	sendMessage({ 2, 13,10 });
	sendMessage({ 2, 14,10 });
	sendMessage({ 2, 3,10 });
	sendMessage({ 2, 3,10 });
	sendMessage({ 2, 3,10 });
	sendMessage({ 2, 5,10 });
	sendMessage({ 2, 5,10 });
	sendMessage({ 2, 5,10 });
	sendMessage({ 2, 13,10 });
	sendMessage({ 2, 3,10 });
	sendMessage({ 2, 5,10 });
	sendMessage({ 2, 5,10 });
	sendMessage({ 2, 5,10 });
	sendMessage({ 2, 3,10 });
	sendMessage({ 2, 3,10 });
	sendMessage({ 2, 3,10 });
	getchar();
	*/
	/*
	cout << "attention" << endl;
	sendMessage({ 2, 15,10 });
	sendMessage({ 2, 4,10 });
	sendMessage({ 2, 7,10 });
	sendMessage({ 2, 15,10 });
	sendMessage({ 2, 4,10 });
	sendMessage({ 2, 7,10 });
	sendMessage({ 2, 15,10 });
	sendMessage({ 2, 4,10 });
	sendMessage({ 2, 7,10 });
	getchar();
	*/
	
	/*
	cout << "sleep" << endl;
	sendMessage({ 2, 13,10 });
	sendMessage({ 2, 16,10 });	
	sendMessage({ 2, 3,10 });	
	sendMessage({ 2, 18,10 });
	getchar();
	*/
	
	
	
	//Maquina estados
	vector<int> sensor;
	for (int i = 0; i < Nsensor; i++)
	{
		sensor.push_back(0);
	}

	vector<vector<double>> reactionInitial(Nstates, vector<double>(Nstates));
	vector<vector<double>> reactionCurrent(Nstates, vector<double>(Nstates));
	reactionInitial = readReaction("files/reactionsInitial.csv");
	/*Descomentar para cada comportamiento*/
	//reactionCurrent = readReaction("files/reactionsExplore.csv");
	reactionCurrent = readReaction("files/reactionsAttention.csv");
	//reactionCurrent = readReaction("files/reactionsGroom.csv");
	//reactionCurrent = readReaction("files/reactionsSleep.csv");
	vector<double> personality(Npersonality);
	personality = readPersonality("files/personality.csv");
	printMatrix(reactionInitial);
	printMatrix(reactionCurrent);
	catState gato(reactionInitial, reactionCurrent, sensor, personality);
	generalState maquina({ 0,0 }, { 0,0 }, {-100,7,7,7,7,7,0,0,0,7,7}, reactionInitial);
	//generalState maquina({ 0,0 }, { 0,0 }, { -100,40,40,7,7,7,7,7,7,7,7 }, reactionInitial);

	while (1) //ejecutar maquina estados
	{
		gato.setSensors(gato.readSensors());
		maquina.checkTransitionState(gato.getSensors(), gato.getCurrentReaction(), gato.getInitialReaction());
		do
		{
			gato.setSensors(gato.readSensors());
			maquina.checkTransitionSubState(gato.getSensors());
			maquina.changeState();
			//gato.setCurrentReaction(maquina.entryActivity(maquina.getCurrentState(), gato.getCurrentReaction(), gato.getInitialReaction()));

		} while (maquina.getCurrentState()[1] != 0);
	}


	
	cout << "Fin";
	return 0;
	
	
}

