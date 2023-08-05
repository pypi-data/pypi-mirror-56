def graphe_evol(base_1,base_2,annee_1,annee_2,var_agg,var_evol):
    import pandas as pd
    import numpy as np
    import networkx as nx
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    base_1['Annee']=annee_1
    base_2['Annee']=annee_2
    d=pd.concat([base_1, base_2], join = 'inner',ignore_index=True)
    assert isinstance(base_1,pd.DataFrame), 'Erreur, la base 1 n est pas de type pd.DataFrame'
    assert isinstance(base_2,pd.DataFrame), 'Erreur, la base 2 n est pas de type pd.DataFrame'
    assert annee_1!=annee_2, 'Erreur, les annees donnees ne sont pas differentes'
    assert var_agg in base_1.columns and var_agg in base_2.columns, 'Erreur : la variable d agregation n est pas dans les deux bases'
    assert var_evol in base_1.columns and var_evol in base_2.columns, 'Erreur : la variable d evolution n est pas dans les deux bases'
    assert type(d[var_agg][1])==str, 'Erreur: vous devez choisir une variable d agregation qualitative'
    assert type(d[var_evol][1])!=str, 'Erreur: vous devez choisir une variable d evolution quantitative (pensez a transtyper)'
    grouped_sd = d.groupby([var_agg,"Annee"])
    gpe=[]
    val_somme=[]
    annee=[]
    effectif=np.array(grouped_sd.size())

    for groupe in grouped_sd:
        gpe.append(groupe[0][0])
        annee.append(groupe[0][1])
        val_somme.append(pd.Series.sum(groupe[1][var_evol]))
    
    d_agg=pd.DataFrame({'GROUPE':gpe, 'ANNEE': annee, 'SOMME': val_somme, 'EFF': effectif})
    
    evol=d_agg.groupby(['GROUPE'])
    gpe=[]
    evolution_var=[]
    evolution_eff=[]
    for groupe in evol:
        if len(groupe[1])==2: #on ne considere que les communes pour lesquelles on a les donnes des deux annees
            gpe.append(groupe[0])    
            mean=np.array(groupe[1]['SOMME'])
            ev=((mean[1]-mean[0])/mean[0])*100
            evolution_var.append(ev)
            mean2=np.array(groupe[1]['EFF'])
            ev2=((mean2[1]-mean2[0])/mean2[0])*100
            evolution_eff.append(ev2)
    tranche_eff=[]
    q1 = np.quantile(evolution_eff,1/4)
    q2 = np.quantile(evolution_eff,1/2)
    q3 = np.quantile(evolution_eff,3/4)
    for x in evolution_eff:
        if x<=q1 : tranche_eff.append(1)
        elif x>q1 and x<=q2 : tranche_eff.append(2)
        elif x>q2 and x<=q3 : tranche_eff.append(3)
        else : tranche_eff.append(4)
    d_agg_evol=pd.DataFrame({'GROUPE':gpe,'EVOL_V': evolution_var,'EVOL_E': evolution_eff, 'TRANCHE_EFF': tranche_eff})

    G=nx.Graph()
    colors=[]
    for i in range(len(d_agg_evol['GROUPE'])):
        G.add_node(i,name=d_agg_evol['GROUPE'][i],evol_v=d_agg_evol['EVOL_V'][i],evol_e=d_agg_evol['EVOL_E'][i],
                   tr=d_agg_evol['TRANCHE_EFF'][i])
        if G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],1/8) : colors.append('royalblue') #arbitraire
        elif G.node[i]['evol_v']>=np.quantile(d_agg_evol['EVOL_V'],1/8) and G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],1/4) : colors.append('lightblue')
        elif G.node[i]['evol_v']==0 : colors.append('grey')
        elif G.node[i]['evol_v']>np.quantile(d_agg_evol['EVOL_V'],1/4) and G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],3/8) : colors.append('palegreen')
        elif G.node[i]['evol_v']>np.quantile(d_agg_evol['EVOL_V'],3/8) and G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],1/2) : colors.append('gold')
        elif G.node[i]['evol_v']>np.quantile(d_agg_evol['EVOL_V'],1/2) and G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],5/8) : colors.append('darkorange')
        elif G.node[i]['evol_v']>np.quantile(d_agg_evol['EVOL_V'],5/8) and G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],3/4) : colors.append('lightpink')
        elif G.node[i]['evol_v']>np.quantile(d_agg_evol['EVOL_V'],3/4) and G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],7/8) : colors.append('tomato')
        else : colors.append('firebrick')
        
    for i in range(len(d_agg_evol['GROUPE'])):
        for j in range(i,len(d_agg_evol['GROUPE'])):
            if G.node[i]['tr']==G.node[j]['tr'] :
                G.add_edge(i, j)

    G1=nx.Graph()
    G2=nx.Graph()
    G3=nx.Graph()
    G4=nx.Graph()
    colors1=[]
    colors2=[]
    colors3=[]
    colors4=[]
    for i in range(len(d_agg_evol['GROUPE'])):
        if G.node[i]['tr']==1:
            G1.add_node(i,name=d_agg_evol['GROUPE'][i],evol_v=d_agg_evol['EVOL_V'][i],evol_e=d_agg_evol['EVOL_E'][i],
            tr=d_agg_evol['TRANCHE_EFF'][i])
            if G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],1/8) : colors1.append('royalblue') #arbitraire
            elif G.node[i]['evol_v']>=np.quantile(d_agg_evol['EVOL_V'],1/8) and G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],1/4) : colors1.append('lightblue')
            elif G.node[i]['evol_v']==0 : colors1.append('grey')
            elif G.node[i]['evol_v']>np.quantile(d_agg_evol['EVOL_V'],1/4) and G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],3/8) : colors1.append('palegreen')
            elif G.node[i]['evol_v']>np.quantile(d_agg_evol['EVOL_V'],3/8) and G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],1/2) : colors1.append('gold')
            elif G.node[i]['evol_v']>np.quantile(d_agg_evol['EVOL_V'],1/2) and G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],5/8) : colors1.append('darkorange')
            elif G.node[i]['evol_v']>np.quantile(d_agg_evol['EVOL_V'],5/8) and G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],3/4) : colors1.append('lightpink')
            elif G.node[i]['evol_v']>np.quantile(d_agg_evol['EVOL_V'],3/4) and G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],7/8) : colors1.append('tomato')
            else : colors1.append('firebrick')

        elif G.node[i]['tr']==2:
            G2.add_node(i,name=d_agg_evol['GROUPE'][i],evol_v=d_agg_evol['EVOL_V'][i],evol_e=d_agg_evol['EVOL_E'][i],
            tr=d_agg_evol['TRANCHE_EFF'][i])
            if G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],1/8) : colors2.append('royalblue') #arbitraire
            elif G.node[i]['evol_v']>=np.quantile(d_agg_evol['EVOL_V'],1/8) and G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],1/4) : colors2.append('lightblue')
            elif G.node[i]['evol_v']==0 : colors2.append('grey')
            elif G.node[i]['evol_v']>np.quantile(d_agg_evol['EVOL_V'],1/4) and G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],3/8) : colors2.append('palegreen')
            elif G.node[i]['evol_v']>np.quantile(d_agg_evol['EVOL_V'],3/8) and G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],1/2) : colors2.append('gold')
            elif G.node[i]['evol_v']>np.quantile(d_agg_evol['EVOL_V'],1/2) and G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],5/8) : colors2.append('darkorange')
            elif G.node[i]['evol_v']>np.quantile(d_agg_evol['EVOL_V'],5/8) and G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],3/4) : colors2.append('lightpink')
            elif G.node[i]['evol_v']>np.quantile(d_agg_evol['EVOL_V'],3/4) and G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],7/8) : colors2.append('tomato')
            else : colors2.append('firebrick')

        elif G.node[i]['tr']==3:
            G3.add_node(i,name=d_agg_evol['GROUPE'][i],evol_v=d_agg_evol['EVOL_V'][i],evol_e=d_agg_evol['EVOL_E'][i],
            tr=d_agg_evol['TRANCHE_EFF'][i])
            if G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],1/8) : colors3.append('royalblue') #arbitraire
            elif G.node[i]['evol_v']>=np.quantile(d_agg_evol['EVOL_V'],1/8) and G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],1/4) : colors3.append('lightblue')
            elif G.node[i]['evol_v']==0 : colors3.append('grey')
            elif G.node[i]['evol_v']>np.quantile(d_agg_evol['EVOL_V'],1/4) and G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],3/8) : colors3.append('palegreen')
            elif G.node[i]['evol_v']>np.quantile(d_agg_evol['EVOL_V'],3/8) and G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],1/2) : colors3.append('gold')
            elif G.node[i]['evol_v']>np.quantile(d_agg_evol['EVOL_V'],1/2) and G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],5/8) : colors3.append('darkorange')
            elif G.node[i]['evol_v']>np.quantile(d_agg_evol['EVOL_V'],5/8) and G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],3/4) : colors3.append('lightpink')
            elif G.node[i]['evol_v']>np.quantile(d_agg_evol['EVOL_V'],3/4) and G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],7/8) : colors3.append('tomato')
            else : colors3.append('firebrick')
        else:
            G4.add_node(i,name=d_agg_evol['GROUPE'][i],evol_v=d_agg_evol['EVOL_V'][i],evol_e=d_agg_evol['EVOL_E'][i],
            tr=d_agg_evol['TRANCHE_EFF'][i])
            if G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],1/8) : colors4.append('royalblue') #arbitraire
            elif G.node[i]['evol_v']>=np.quantile(d_agg_evol['EVOL_V'],1/8) and G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],1/4) : colors4.append('lightblue')
            elif G.node[i]['evol_v']==0 : colors4.append('grey')
            elif G.node[i]['evol_v']>np.quantile(d_agg_evol['EVOL_V'],1/4) and G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],3/8) : colors4.append('palegreen')
            elif G.node[i]['evol_v']>np.quantile(d_agg_evol['EVOL_V'],3/8) and G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],1/2) : colors4.append('gold')
            elif G.node[i]['evol_v']>np.quantile(d_agg_evol['EVOL_V'],1/2) and G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],5/8) : colors4.append('darkorange')
            elif G.node[i]['evol_v']>np.quantile(d_agg_evol['EVOL_V'],5/8) and G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],3/4) : colors4.append('lightpink')
            elif G.node[i]['evol_v']>np.quantile(d_agg_evol['EVOL_V'],3/4) and G.node[i]['evol_v']<np.quantile(d_agg_evol['EVOL_V'],7/8) : colors4.append('tomato')
            else : colors4.append('firebrick')
            
    mapping = dict(zip(G,d_agg_evol['GROUPE']))
    G = nx.relabel_nodes(G, mapping)   
    mapping1 = dict(zip(G1,d_agg_evol['GROUPE'][np.ravel(np.where(np.array(tranche_eff)==1))]))
    G1 = nx.relabel_nodes(G1, mapping1)
    mapping2 = dict(zip(G2,d_agg_evol['GROUPE'][np.ravel(np.where(np.array(tranche_eff)==2))]))
    G2 = nx.relabel_nodes(G2, mapping2)
    mapping3 = dict(zip(G3,d_agg_evol['GROUPE'][np.ravel(np.where(np.array(tranche_eff)==3))]))
    G3 = nx.relabel_nodes(G3, mapping3)
    mapping4 = dict(zip(G4,d_agg_evol['GROUPE'][np.ravel(np.where(np.array(tranche_eff)==4))]))
    G4 = nx.relabel_nodes(G4, mapping4)


    royalblue_patch = mpatches.Patch(color='royalblue',label='Evolution inferieure a '+str(round(np.quantile(d_agg_evol['EVOL_V'],1/8)))+'%')
    lightblue_patch = mpatches.Patch(color='lightblue', label='Evolution comprise entre '+str(round(np.quantile(d_agg_evol['EVOL_V'],1/8)))+ ' et '+ str(round(np.quantile(d_agg_evol['EVOL_V'],2/8)))+'%')
    palegreen_patch = mpatches.Patch(color='palegreen', label='Evolution comprise entre '+str(round(np.quantile(d_agg_evol['EVOL_V'],2/8)))+ ' et '+ str(round(np.quantile(d_agg_evol['EVOL_V'],3/8)))+'%')
    gold_patch = mpatches.Patch(color='gold', label='Evolution comprise entre '+str(round(np.quantile(d_agg_evol['EVOL_V'],3/8)))+ ' et '+ str(round(np.quantile(d_agg_evol['EVOL_V'],4/8)))+'%')
    darkorange_patch = mpatches.Patch(color='darkorange', label='Evolution comprise entre '+str(round(np.quantile(d_agg_evol['EVOL_V'],4/8)))+ ' et '+ str(round(np.quantile(d_agg_evol['EVOL_V'],5/8)))+'%')
    lightpink_patch = mpatches.Patch(color='lightpink', label='Evolution comprise entre '+str(round(np.quantile(d_agg_evol['EVOL_V'],5/8)))+ ' et '+ str(round(np.quantile(d_agg_evol['EVOL_V'],6/8)))+'%')
    tomato_patch = mpatches.Patch(color='tomato', label='Evolution comprise entre '+str(round(np.quantile(d_agg_evol['EVOL_V'],6/8)))+ ' et '+ str(round(np.quantile(d_agg_evol['EVOL_V'],7/8)))+'%')
    firebrick_patch = mpatches.Patch(color='firebrick',label='Evolution superieure a '+str(round(np.quantile(d_agg_evol['EVOL_V'],7/8)))+'%')

    fig, axes = plt.subplots(nrows=3, ncols=2,figsize=(30,30))
    ax = axes.flatten()
    pos = nx.spring_layout(G,k=0.25,iterations=20)

    nx.draw(G,pos,with_labels=False,node_size=100,node_color=colors,ax=ax[0])
    ax[0].set_title("Vue globale de l'evolution de la variable "+var_evol+ " par "+var_agg +" entre "+str(d['Annee'].unique()[0])+" et "+str(d['Annee'].unique()[1]),fontweight="bold")
    ax[0].legend(handles=[royalblue_patch,lightblue_patch,palegreen_patch,gold_patch,darkorange_patch,lightpink_patch,tomato_patch,firebrick_patch])
    ax[0].set_axis_off()

    if G1.number_of_nodes()>0 :
        nx.draw_spring(G1,with_labels=True,fontsize=5,node_size=500,node_color=colors1,ax=ax[1])
        ax[1].set_title("Evolution de "+var_evol+ " pour les "+var_agg+" \n dont l'effectif a evolue de moins de " +str(round(np.quantile(evolution_eff,1/4)))+"%",fontweight="bold")
        #ax[1].legend(handles=[royalblue_patch,lightblue_patch,palegreen_patch,gold_patch,darkorange_patch,lightpink_patch,tomato_patch,firebrick_patch])
    ax[1].set_axis_off()

    if G2.number_of_nodes()>0 :
        nx.draw_spring(G2,with_labels=True,fontsize=5,node_size=500,node_color=colors2,ax=ax[2])
        ax[2].set_title("Evolution de "+var_evol+ " pour les "+var_agg+" \n dont l'effectif a evolue entre " +str(round(np.quantile(evolution_eff,1/4)))+" et "+str(round(np.quantile(evolution_eff,2/4)))+"%",fontweight="bold")
        #ax[2].legend(handles=[royalblue_patch,lightblue_patch,palegreen_patch,gold_patch,darkorange_patch,lightpink_patch,tomato_patch,firebrick_patch])
    ax[2].set_axis_off()

    if G3.number_of_nodes()>0 : 
        nx.draw_spring(G3,with_labels=True,fontsize=5,node_size=500,node_color=colors3,ax=ax[3])
        ax[3].set_title("Evolution de "+var_evol+ " pour les "+var_agg+" \n dont l'effectif a evolue entre " +str(round(np.quantile(evolution_eff,2/4)))+" et "+str(round(np.quantile(evolution_eff,3/4)))+"%",fontweight="bold")
        #ax[3].legend(handles=[royalblue_patch,lightblue_patch,palegreen_patch,gold_patch,darkorange_patch,lightpink_patch,tomato_patch,firebrick_patch])
    ax[3].set_axis_off()
    
    if G4.number_of_nodes()>0 :
        nx.draw_spring(G4,with_labels=True,fontsize=5,node_size=500,node_color=colors4,ax=ax[4])
        ax[4].set_title("Evolution de "+var_evol+ " pour les "+var_agg+" \n dont l'effectif a evolue de plus de " +str(round(np.quantile(evolution_eff,3/4)))+"%",fontweight="bold")
        #ax[4].legend(handles=[royalblue_patch,lightblue_patch,palegreen_patch,gold_patch,darkorange_patch,lightpink_patch,tomato_patch,firebrick_patch])
    ax[4].set_axis_off()
    ax[5].set_axis_off()

    plt.savefig("graphe_evol.png")