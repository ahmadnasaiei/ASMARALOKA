df_edge = pd.DataFrame({'Title': title, 'Location': location, 'Price': price, 'Area': sqft,
                       'Bedroom': bedroom, 'Bathroom': bathroom, 'Agent Name': agent_name, 'Phone Number': agent_phone_no})
print(df_edge)

df_edge.to_excel('edgeprop_property.xlsx', index=False)