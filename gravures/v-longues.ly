\version "2.24.3"
%% Fichier produit par outils/generer_valeurs.py — ne pas modifier à la main.
\paper {
  indent = 0
  ragged-right = ##t
  top-margin = 1\mm
  bottom-margin = 1\mm
  left-margin = 1\mm
  right-margin = 1\mm
  oddHeaderMarkup = ##f
  evenHeaderMarkup = ##f
  oddFooterMarkup = ##f
  evenFooterMarkup = ##f
  bookTitleMarkup = ##f
  scoreTitleMarkup = ##f
}
\score {
  \new Staff {
    \clef treble \numericTimeSignature \autoBeamOff \textLengthOn
    \override TextScript.staff-padding = #2.5
    \override MultiMeasureRestText.staff-padding = #2.5
    \time 4/2
    a'\breve_\markup \small \italic \override #'(baseline-skip . 2.4) \center-column { "carrée" } | r\breve_\markup \small \italic \override #'(baseline-skip . 2.4) \center-column { "bâton de" "pause" } \bar "||"
    \time 4/4
    \compressMMRests { R1*8_\markup \small \italic \override #'(baseline-skip . 2.4) \center-column { "mesures à" "compter" } } | c''4 d'' e'' f'' \bar "|."
  }
  \layout { \context { \Score \override SpacingSpanner.spacing-increment = #1.6 } }
}
