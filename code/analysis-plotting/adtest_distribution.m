%%
path = '/Users/ivan/Documents/aaa_online_stuff/coding/python/phd/expt17_spots/data/spots_locations/per_participant';
folders = dir(strcat(path, '/*.csv'));
uniform_dist = makedist('uniform', 'Lower', 0, 'Upper', 1200);

%%
ads_ps = zeros(8, 3);
for subject=1:size(folders, 1)
    file_path = [path '/' folders(subject).name];
    table = readtable(file_path);
    x_axis = table.Var1;
    x_axis = x_axis(2:end);
    disp(round(max(x_axis) + 50, -2))
    
    [h,p,adstat,cv] = adtest(x_axis, 'Distribution', uniform_dist);
    ads_ps(subject, 1) = subject;
    ads_ps(subject, 2) = p;
    ads_ps(subject, 3) = adstat;

end

disp(ads_ps)

save('/Users/ivan/Documents/aaa_online_stuff/coding/python/phd/expt17_spots/data/adtest.mat','ads_ps');
dlmwrite('/Users/ivan/Documents/aaa_online_stuff/coding/python/phd/expt17_spots/data/adtest.txt',ads_ps);
% dlmwrite('filename.txt',a)
